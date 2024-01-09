from pandas import DataFrame, read_sql, concat
from sqlite3 import connect
from pathlib import Path
import pyomo.environ as pe

def Keyzer(df : DataFrame, cols : list = [], valcol : str = "") -> dict:
	return dict(zip(df[cols].to_records(index=False).tolist(), df[valcol]))

def extract_subdata(data: dict,substring : str) -> dict:
    subdata = {}
    for key, value in data.items():
        if substring in key[0]:
            subdata[key[1]] = value
    return subdata

def readfromDB(query:str) -> DataFrame:
    dbpath: Path = Path(__file__).parent.parent / 'db.sqlite3'
    with connect(dbpath.absolute()) as connection:
        return read_sql(query, connection)
    
def executeQueryDB(query: str):
    dbpath: Path = Path(__file__).parent.parent / 'db.sqlite3'
    with connect(dbpath.absolute()) as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()

def write2DB(df:DataFrame, tablename:str, test:bool = False, optimize: bool = True) -> bool:
    if tablename == '':
        return False  
    if not test:
        dbpath: Path = Path(__file__).parent.parent / 'db.sqlite3'
    else:
        dbpath: Path = Path(__file__).parent.parent / 'test.sqlite3'
    with connect(dbpath.absolute()) as connection:
            if optimize:
                df.to_sql(tablename, connection, index=False, if_exists='replace')  # Reemplazar datos durante optimizacion
            else:
                df.to_sql(tablename, connection, index=False, if_exists='append')  # Agragar datos cuando hayan cambios
    return True

def getDisableParams(enabledfparams:dict):
    # Roles predefinidos
    predefined_role_paramaters = {
        'MaxChanges': ['Electrico', 'Energetico'],
        'MinAnalist': ['Electrico', 'Energetico'],
        'MinDays': ['Electrico', 'Energetico'],
        'MinXp': ['Electrico', 'Energetico'],
        'MinOutWork': ['Electrico', 'Energetico']
    }

    disableParams = {}
    # Comprobar las parametros que estan activos en el dataframe, los que nos se guardan para desactivar la restriccion
    for param, roles in predefined_role_paramaters.items():
        if param not in enabledfparams:
            disableParams[param] = roles
        else:
            missing_roles = list(set(roles) - set(enabledfparams[param]))
            if missing_roles:
                disableParams[param] = missing_roles
    return disableParams

def lookforConstants(dfconstants):
    # Constantes predefinidas
    predefined_constants = {
        'FINALDAY': 30,
        'SATURDAY': 5,
        'NEXTWEEKEND': 7,
        'PENALIZATION': 30,
    }

    for constant, value in predefined_constants.items():
        if constant not in dfconstants['name'].values:
            new_row = {'name': constant, 'value': value}
            dfconstants = concat([dfconstants, DataFrame([new_row])], ignore_index=True)
            
    return dfconstants

def deactivateConstraintsByRoles(sch, disableParams: dict):
    # Mapeo de parametros a Restricciones
    paramXConstr = {        
        'MaxChanges': 'cNoAlterInDispach',
        'MinAnalist': 'cMinWorkers',
        'MinDays': 'cContinuousShift',
        'MinXp': 'cMinExpDay',
        'MinOutWork': 'cContinuousShiftRest'
    }

    # Diccionario de Restricciones desactivadas apartir de los parametros desactivados
    disableConstr = {paramXConstr[key]: value for key, value in disableParams.items() if key in paramXConstr}

    # Iterar todas las restricciones del modelo
    for constraint in sch.component_objects(pe.Constraint):
        # Comprobar si la restriccion actual esta en disableConstr
        if constraint.name in disableConstr:
            # Lista de los roles a desactivar asociados a restriccion 
            roles_to_deactivate = disableConstr[constraint.name]
            # Iterar sobre todos los roles a desactivar
            for role_to_deactivate in roles_to_deactivate:
                # Iterar entre indices y valores de las restricciones
                for index, value in constraint.items():
                    # Comprorar que el rol actual hace parte del indice
                    if role_to_deactivate in index:
                        # Desactivar la restriccion especifica asociada a ese rol
                        constraint[index].deactivate()
                        print(f"Desactivado {constraint.name} en {index}")

    if not disableConstr:
        return None
    else:
        return disableConstr
    
    
def deactivateConstraint(sch, disableConstrain = None):
    # Mapeo de parametros a Restricciones
    constraints = ['cAuxMaxDays', 'cCountDays', 'cCountShifts', 'cMinWorkers', 'cMinExpDay', 'cAuxShiftStart', 'cAuxNoDualBoth', 'cAuxNoDualRol', 'cContinuousShift', 'cContinuousShiftRest', 'cNoAlterInDispach', 'cContinuosShiftWeekend', 'cNConseWeekendDays', 'cExpRetention']
    if disableConstrain:
        # Iterar todas las restricciones del modelo
        for constraint in sch.component_objects(pe.Constraint):
            # Comprobar si la restriccion actual esta en disableConstr
            if constraint.name in disableConstrain:
                constraint.deactivate()
                print(f"Desactivado {constraint.name}")


def getSchedule()-> DataFrame:
    query = '''
    SELECT
        SUBSTR(sw.name, 1, INSTR(sw.name, ' ') - 1) || '' || SUBSTR(sw.name, INSTR(sw.name, ' '), 2) as name,
        ssr.day,
        ssr.rol,
        swe.experience
    FROM
        (SELECT WORKER_ID, strftime('%d', `daydate`) as day, ROL FROM schedule_schedule_results) as ssr
    INNER JOIN
        schedule_worker AS sw 
    ON ssr.worker_id = sw.id
    INNER JOIN
        schedule_workerexperience AS swe 
    ON sw.id = swe.worker_id
    INNER JOIN
        schedule_role AS sr 
    ON ssr.rol = sr.name AND swe.role_id = sr.id
    ORDER BY
        ssr.day;
    '''
    return readfromDB(query)

def getWorkers() -> DataFrame:
    querysql = 'SELECT NAME, WEIGHT, ID FROM SCHEDULE_WORKER'
    return readfromDB(querysql)

def getConstants() -> DataFrame:
    querysql = 'SELECT NAME, VALUE FROM SCHEDULE_CONSTANTS'
    return readfromDB(querysql)

def getRoles() -> DataFrame:
    querysql = 'SELECT NAME FROM SCHEDULE_ROLE'
    return readfromDB(querysql)

def getParams() -> DataFrame:
    querysql = f'''
        SELECT
            PARAMETER, VALUE, NAME as role_name, SP.ID
        FROM 
            SCHEDULE_PARAMETERS as SP
        INNER JOIN
            (SELECT NAME, id FROM SCHEDULE_ROLE) as SR
        ON SP.ROLE_ID = SR.ID
        '''
    return readfromDB(querysql)

def getEnableParams(model_params) -> DataFrame:
    selected_params = model_params.get('params', {})
    selected_params_list = []
    for param_id, is_selected in selected_params.items():
        if is_selected:
            selected_params_list.append(param_id)

    sel_params_str = ','.join(map(str, selected_params_list))
    querysql = f'''
        SELECT
            PARAMETER, VALUE, NAME as role_name, SP.ID
        FROM 
            SCHEDULE_PARAMETERS as SP
        INNER JOIN
            (SELECT NAME, id FROM SCHEDULE_ROLE) as SR
        ON SP.ROLE_ID = SR.ID
        WHERE SP.ID IN ({sel_params_str})
        '''
    return readfromDB(querysql)

def getWorkerExperience() -> DataFrame:
    querysql = '''
        SELECT 
            SWE.EXPERIENCE, SR.NAME AS role_name, SW.NAME AS worker_name
        FROM 
            SCHEDULE_WORKEREXPERIENCE AS SWE
        INNER JOIN
            SCHEDULE_ROLE AS SR
        ON
            SWE.ROLE_ID = SR.ID
        INNER JOIN
            SCHEDULE_WORKER AS SW
        ON
            SWE.WORKER_ID = SW.ID;
        '''
    return readfromDB(querysql)


def getScheduleDetails()-> DataFrame:
    query = ''' 
    SELECT
        SUBSTR(sw.name, 1, INSTR(sw.name, ' ') - 1) || '' || SUBSTR(sw.name, INSTR(sw.name, ' '), 2) as name,
        COUNT(DISTINCT ssr.daydate) as total_days,
        COUNT(DISTINCT ssr.daydate) * sw.weight as workload
    FROM
        (SELECT worker_id, daydate, ROL FROM schedule_schedule_results) as ssr
    INNER JOIN
        (SELECT name, id, weight FROM schedule_worker) as sw
    ON ssr.worker_id = sw.id
    GROUP BY ssr.worker_id, name;
    '''
    return readfromDB(query)