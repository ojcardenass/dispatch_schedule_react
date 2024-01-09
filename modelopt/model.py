from .params import *
from pandas import unique, DataFrame, concat
from pyomo.opt import SolverFactory, SolverStatus, TerminationCondition
from pyomo.util.infeasible import log_infeasible_constraints
from datetime import datetime, timedelta
import logging
import pyomo.environ as pe

# 
def executemodel(model_params,solver_opt, disableConstrain = None, test = False):

    # Diccionario de Mensajes
    solver_messages = {}

    # Modelo concreto de Pyomo llamado sch
    sch = pe.ConcreteModel()
    sch.name = 'schedule optimization'

    #Dia de referencia
    REFDAY = datetime(2023,1,1)
    
    #TODO Diciembre: Condiciones iniciales, Forzar estado de turno por dia,persona y rol, Usar calendario para dia de referencia

    # Obtener parametros y constantes de las bases de datos
    dfparams = getParams()
    dfconstants = getConstants()
    enadfparams = getEnableParams(model_params).groupby('parameter')['role_name'].apply(list).to_dict()

    # Obtener los parametros desactivados y las constantes faltantes
    disableParams = getDisableParams(enadfparams)
    lookforConstants(dfconstants)


    # Constant
    ONE = 1
    constants = Keyzer(dfconstants,['name'],'value')


    # Sets
    dfworkers=getWorkers()
    dfroles = getRoles()
    sch.sWorkers = pe.Set(initialize=unique(dfworkers['name']))
    sch.sDays = pe.Set(initialize=range(ONE,constants[('FINALDAY',)]+ONE,ONE))
    sch.sRoles = pe.Set(initialize=unique(dfroles['name']))


    # Params - preprocess
    dfworkexp = getWorkerExperience()
    pWeights = Keyzer(dfworkers,['name'],'weight')
    pWorkerId = Keyzer(dfworkers,['name'],'id')
    pWorkerXp = Keyzer(dfworkexp,['worker_name','role_name'],'experience')
    
    paramsDict = Keyzer(dfparams,['parameter','role_name'],'value')
    pMinWorkersRoles = extract_subdata(paramsDict,"MinAnalist")
    pMinDaysRoles = extract_subdata(paramsDict,"MinDays")
    pMinXpRoles = extract_subdata(paramsDict,"MinXp")
    pMaxChangesRoles = extract_subdata(paramsDict,"MaxChanges")
    pMinOutWorkRoles = extract_subdata(paramsDict,"MinOutWork")


    # Params
    sch.pWeights = pe.Param(sch.sWorkers, initialize=pWeights, within=pe.NonNegativeIntegers, default=100)
    sch.pWorkerId = pe.Param(sch.sWorkers, initialize=pWorkerId, within=pe.NonNegativeIntegers)
    sch.pWorkerXp = pe.Param(sch.sWorkers, sch.sRoles, initialize=pWorkerXp, within=pe.NonNegativeIntegers)
    ## Params dependientes del rol
    sch.pMinXpRoles = pe.Param(sch.sRoles, initialize= pMinXpRoles, within= pe.NonNegativeIntegers)
    sch.pMinWorkersRoles = pe.Param(sch.sRoles, initialize= pMinWorkersRoles, within= pe.NonNegativeIntegers)
    sch.pMinDaysRoles = pe.Param(sch.sRoles, initialize= pMinDaysRoles, within= pe.NonNegativeIntegers)
    sch.pMaxChangesRoles = pe.Param(sch.sRoles, initialize= pMaxChangesRoles, within= pe.NonNegativeIntegers)
    sch.pMinOutWorkRoles = pe.Param(sch.sRoles, initialize= pMinOutWorkRoles, within= pe.NonNegativeIntegers)


    # Vars
    sch.vbAssignment = pe.Var(sch.sWorkers, sch.sDays, sch.sRoles, within=pe.Binary)
    sch.vbBeAssignment = pe.Var(sch.sWorkers, sch.sDays, within=pe.NonNegativeReals)
    sch.vWorkingDays = pe.Var(sch.sWorkers, within=pe.PositiveReals)
    sch.vMaxWeight = pe.Var(within=pe.PositiveReals)
    sch.vbShiftStart = pe.Var(sch.sWorkers, sch.sDays,sch.sRoles, within=pe.Binary)
    sch.vbShiftEnd = pe.Var(sch.sWorkers, sch.sDays,sch.sRoles, within=pe.Binary)
    sch.vbExpPenal = pe.Var(sch.sWorkers, sch.sRoles, within=pe.Binary)

    # Objetive Function
    def objFun(m):
        return m.vMaxWeight + sum([constants[('PENALIZATION',)] * m.vbExpPenal[c,r] for c in m.sWorkers for r in m.sRoles])
    sch.obj = pe.Objective(rule=objFun, sense=pe.minimize, doc='Minimización del maximo peso con penalización de retención de experiencia')
    

    # Restrictions
    ## Maximo de días ponderados
    def maxLaboDays(m, c):
        return m.vMaxWeight >= m.pWeights[c] * m.vWorkingDays[c]
    sch.cAuxMaxDays = pe.Constraint(sch.sWorkers, rule=maxLaboDays, doc= "Restriccion auxiliar para identificar a la persona con mayor acumulado de trabajo")
    
    ## Numero de dias trabajados al mes, por cada trabajador
    def sumDays(m, c):
        return m.vWorkingDays[c] == sum([ m.vbAssignment[c,d,r] for d in m.sDays for r in m.sRoles])
    sch.cCountDays = pe.Constraint(sch.sWorkers, rule=sumDays, doc="Restriccion de cantidad de dias trabajados por el trabajador")

    ## Turno al dia, sin importar el rol
    def sumShifts(m, c, d):
        return m.vbBeAssignment[c,d] == sum([ m.vbAssignment[c,d,r] for r in m.sRoles])
    sch.cCountShifts = pe.Constraint(sch.sWorkers, sch.sDays, rule=sumShifts, doc="Restricción auxiliar para contar la cantidad de días en turno en cualquier rol")

    ## Minimo numero de trabajadores por día
    def minWorkersDay(m, d, r):
        return sum([ m.vbAssignment[c,d,r] for c in m.sWorkers ]) == m.pMinWorkersRoles[r]
    sch.cMinWorkers = pe.Constraint(sch.sDays, sch.sRoles, rule=minWorkersDay, doc="Restriccion del minimo de trabajadores por día")

    ## Minimo valor de experiencia por día
    def minExpDay(m, d, r):
        return sum([ m.vbAssignment[c,d,r] * m.pWorkerXp[c,r] for c in m.sWorkers ]) >= m.pMinXpRoles[r]
    sch.cMinExpDay = pe.Constraint(sch.sDays, sch.sRoles, rule=minExpDay, doc="Restricción del mínimo de experiencia por día")

    ## Restriccion auxiliar de inicio de turno
    def shiftInit(m,c,d,r):
        if d > ONE:
            return m.vbShiftEnd[c, d, r] - m.vbShiftStart[c, d, r] == m.vbAssignment[c, d-ONE, r] - m.vbAssignment[c, d, r]
        return pe.Constraint.Skip
    sch.cAuxShiftStart = pe.Constraint(sch.sWorkers, sch.sDays, sch.sRoles, rule=shiftInit, doc = "Restriccion auxiliar para marcar el inicio de turno" )

    ## Restriccion auxiliar de no simultaneidad de estados de turno
    def NoDualBoth(m,c,d,r):
        return m.vbShiftEnd[c, d, r] + m.vbShiftStart[c, d, r] <= ONE
    sch.cAuxNoDualBoth = pe.Constraint(sch.sWorkers, sch.sDays, sch.sRoles, rule=NoDualBoth, doc = "Restriccion auxiliar para evitar que tanto el final y el inicio de turno se den simultaneamente" )

    ## Restriccion auxiliar de no simultaneidad de estados de rol
    def NoDualRol(m,c,d):
        return sum([ m.vbAssignment[c,d,r] for r in m.sRoles ]) <= ONE
    sch.cAuxNoDualRol = pe.Constraint(sch.sWorkers, sch.sDays, rule=NoDualRol, doc = "Restricción auxiliar para evitar que un trabajador tenga simultaneamente varios roles" )

    ## Minimo de tiempo de dias consecutivos en turno
    def continuousShift(m, c, d, r):
        return sum([m.vbAssignment[c,d+p,r] for p in range(m.pMinDaysRoles[r]) if d+p <= constants[('FINALDAY',)]]) >= m.pMinDaysRoles[r] * m.vbShiftStart[c,d,r]
    sch.cContinuousShift = pe.Constraint(sch.sWorkers, sch.sDays,sch.sRoles, rule=continuousShift, doc="Restriccion de k turnos continuos")

    ## Tiempo minimo fuera de turno
    def continuousShiftRest(m, c, d, r):
        return sum([m.vbAssignment[c,d+h,r] for h in range(m.pMinOutWorkRoles[r]) if d+h <= constants[('FINALDAY',)]]) <= (m.pMinOutWorkRoles[r]) * (1 - m.vbShiftEnd[c,d,r])
    sch.cContinuousShiftRest = pe.Constraint(sch.sWorkers, sch.sDays, sch.sRoles, rule=continuousShiftRest, doc="Restriccion de h dias de descanso despues de turnos continuos")

    ## Continuidad del despacho
    def noAlterInDispach(m, d, r):
        return sum([m.vbShiftEnd[c,d,r] for c in m.sWorkers]) <= m.pMaxChangesRoles[r]
    sch.cNoAlterInDispach = pe.Constraint(sch.sDays,sch.sRoles, rule=noAlterInDispach, doc="Restriccion de a lo sumo c cambios en las personas asignadas a turno")

    ## Fines de semana
    def continuousShiftWeekend(m, c, d):
        if (REFDAY + timedelta(days=d-ONE)).weekday() == constants[('SATURDAY',)] and d+ONE <= constants[('FINALDAY',)]:
            return m.vbBeAssignment[c,d] == m.vbBeAssignment[c,d+ONE]
        else:
            return pe.Constraint.Skip
    sch.cContinuosShiftWeekend = pe.Constraint(sch.sWorkers, sch.sDays, rule=continuousShiftWeekend, doc="Restriccion de turno continuo en fines de semana")

    ## Numero de fines de semana consecutivos trabajados al mes, por cada trabajador
    def noConsecutiveWeekendDays(m, c, d):
        if (REFDAY + timedelta(days=d-ONE)).weekday() == constants[('SATURDAY',)] and d+constants[('NEXTWEEKEND',)] <= constants[('FINALDAY',)]:
            return m.vbBeAssignment[c,d] + m.vbBeAssignment[c,d+constants[('NEXTWEEKEND',)]] <= ONE
        else:
            return pe.Constraint.Skip
    sch.cNConseWeekendDays = pe.Constraint(sch.sWorkers,sch.sDays, rule=noConsecutiveWeekendDays, doc="Restricción para limitar asignaciones en fines de semana por el trabajador")

    ## Restriccion suave retención de experiencia en turno
    def expRetention(m, c, r):
        value = sum([m.vbAssignment[c,d,r] for d in m.sDays])
        return value >= 1 - m.vbExpPenal[c,r]
    sch.cExpRetention = pe.Constraint(sch.sWorkers,sch.sRoles, rule=expRetention, doc="Restricción suave para asegurar que cada trabajador realice un turno por lo menos una vez cada mes")

    ## Compensatorio de dominicales en semana
    def sundayCompenRest(m, c, d):
        if (REFDAY + timedelta(days=d-ONE)).weekday() == 6:
            return sum([m.vbBeAssignment[c,d+h] for h in range(15) if d+h <= constants[('FINALDAY',)] ]) <= 15 - (3 * m.vbBeAssignment[c,d])
        else:
            return pe.Constraint.Skip
    sch.cSundayCompenRest = pe.Constraint(sch.sWorkers, sch.sDays, rule=sundayCompenRest, doc="Restriccion de h dias de descanso despues de turnos continuos")


    # Desactivar Restricciones por Rol y obtener diccionario de restricciones desactivadas
    disableConstr = deactivateConstraintsByRoles(sch,disableParams)
    deactivateConstraint(sch,disableConstrain)
    
    #sch.cSundayCompenRest.deactivate() 
    #sch.cContinuousShift.deactivate() 
    #sch.cContinuousShiftRest.deactivate()
    sch.write('sch.lp', io_options={'symbolic_solver_labels': True})

    # Seleccion del solver
    # opt = SolverFactory("cplex", executable=r'\\comedxmv209\ILOG\ODME35\cplex\bin\x86_win32\cplex.exe')
    opt = SolverFactory("cplex", executable=r'D:\Pruebas\cplex\bin\x86_win32\cplex.exe')
    

    solver_options = {'mipgap': solver_opt['mipgap'], 
                      'timelimit': solver_opt['timelimit'], 
                      'workdir': str(Path(__file__).parent.parent.absolute()),
                      'logfile': 'sch.log'                   
                    #   'threads': 4,
                      }
    opt.set_options(solver_options)

    results = opt.solve(sch, tee=True) 

    # print(" ")
    # print("Day", "A_{n,t}","Z_{n,t}", "Y_{n,t}", "B_{n,t}", "Rol", sep= " | ")
    # for w in sch.sWorkers:
    #     if w != "Jaime Hernandez Sanchez":
    #         continue
    #     for r in sch.sRoles:
    #         for d in sch.sDays:
    #             #print(w,d)
    #             print(f"{d:>02}", sch.vbAssignment[w,d,r].value,sch.vbShiftStart[w,d,r].value, sch.vbShiftEnd[w,d,r].value, sch.vbBeAssignment[w,d].value, r, sep= " | ")   

    # Manejo de los estados del solver
    if results.solver.termination_condition == TerminationCondition.infeasible:
        root_logger= logging.getLogger()
        root_logger.setLevel(logging.DEBUG) # or whatever
        handler = logging.FileHandler('infes.log', 'w', 'utf-8') # or whatever
        handler.setFormatter(logging.Formatter('%(name)s %(message)s')) # or whatever
        root_logger.addHandler(handler)
        log_infeasible_constraints(sch, log_expression=True, log_variables=True)
        # print('Infeasible constraints logged')

        solver_messages["status"] = "Solution infeasible"
        solver_messages["solver_info"] = str(results.solver)
        solver_messages["message"] = "Do something about it? or exit?"
        data2DBStatus = False
        dfdic = DataFrame()
        return data2DBStatus, solver_messages, dfdic
    elif (results.solver.status == SolverStatus.ok) and (results.solver.termination_condition == TerminationCondition.optimal):
        solver_messages["status"] = "Solution feasible and optimal"
        solver_messages["obj_vale"] = f'Objective function value: $ {sch.obj.expr():,.4f}'
        solver_messages["message"] = f'Restrictions deactivated: {disableConstr}'
    else:
        solver_messages["status"] = "Warning!!"
        solver_messages["message"] = "*** The problem seems a little complicated, dont trust this solution ***"
        solver_messages["solver_info"] = str(results.solver)

    # Post-process

    ans = [[ONE, REFDAY + timedelta(days= d - ONE),r,sch.pWorkerId[w]] for w in sch.sWorkers for r in sch.sRoles for d in sch.sDays if sch.vbAssignment[w,d,r].value > 0]
    
    dfans = DataFrame(ans,columns=['value','daydate','rol','worker_id'])

    data2DBStatus = write2DB(dfans,'schedule_schedule_results',test) #'schedule_schedule_results' 
    
    ans = [[sch.vbAssignment[w,d,r].value,d ,r,w] for w in sch.sWorkers for r in sch.sRoles for d in sch.sDays]
    dfans = DataFrame(ans,columns=['value','daydate','rol','worker_id']).pivot(index=['worker_id','rol'], columns='daydate', values='value')
    dfans.to_csv('ans.csv')
    dfdic = dfans.to_dict()
    dfdic['Weekends'] = [d for d in sch.sDays if (REFDAY + timedelta(days=d-ONE)).weekday() == constants[('SATURDAY',)]]
    dfdic['Weekends'] = [d for d in dfdic['Weekends'] for d in [d,d+1]]

    print(Path(__file__).parent.parent.absolute() )

    return data2DBStatus, solver_messages, dfdic

if __name__ == '__main__':
    executemodel()