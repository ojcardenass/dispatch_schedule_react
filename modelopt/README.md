# Conjuntos

$N \in 1 .. n \space$ : $\quad$ Empleados   
$t \in 1 .. T \space$ : $\quad$ Días  
$r \in 1 .. R \space$ : $\quad$ Roles 

# Constantes

$D$ : $\quad$ Maximo número de dias

# Parametros
$W_{n} \in \mathbb{R}^{+}$: $\quad$ Peso del empleado $n$.   
$\nu_{n,r} \in \mathbb{N}$: $\quad$ Experiencia del empleado $n$ en el rol $r$.  
$\omega_{r} \in \mathbb{N}$: $\quad$ Mínimo número de asignaciones diarias en el rol $r$.  
$\tau_{r} \in \mathbb{N}$: $\quad$ Mínimo valor de experiencia total en turno por cada rol.    
$k \in \mathbb{N}$: $\quad$ Número de días consecutivos en turno.       
$c \in \mathbb{N}\space$ : $\quad$ Número de cambios de personas asignadas en turno.   
$\phi \in \mathbb{N}\space$ : $\quad$ Constante para agravar la penalización $P_n$.  

# Variables

$A_{n,t,r} \in \{0,1\} \space $: $\quad$ Asignación de turno, 1 si el Trabajador $n$ trabaja el día $t$ en el rol $r$.   
$B_{n,t} \in \{0,1\} \space $: $\quad$ Variable auxiliar para contar si el empleado esta en turno, indiferente del rol.   
$X_n \in \mathbb{N} \space $: $\quad$ Dias asignados a empleado $n$.     
$X^{w} \in \mathbb{R} \space$: $\quad$ Máxima carga de los compas.    
$Z_{n,t,r} \in \{0,1\} \space$ : $\quad$ Inicio de turnos, 1 si el trabajador $n$ inicia turno el día $t$ en el rol $r$.   
$Y_{n,t,r} \in \{0,1\} \space$ : $\quad$ Fin de turnos, 1 si el trabajador $n$ no inicia turno el día $t$ en el rol $r$.   
$P_{n,r} \in \mathbb{N} \space$ : $\quad$ Variable para habilitar la penalización de retención de experiencia, 1 si el trabajador $n$ no realiza turno en el mes.      

# Función objetivo
 - Distribuir la carga pondera de trabajo entre los compañeros del turno
 - Minimizar al compañero que más carga tenga

<!-- $\min_{z} \sum_{n} A_{n}N_{n}X_{n}$ -->
$\min_{z}:$ $X^{w} +  \phi\cdot \displaystyle\sum_nP_{n,r} $ 

# Restricciones

### Compañero que mas carga tiene

- Identifica la mayor carga de los compañeros

$X^{w} \ge X_{n} \cdot W_{n} \quad \forall n \in N $

### Conteo de días laborados del compañero
- Restricción de cantidad de dias laborados por el trabajador

$X_{n} = \displaystyle\sum_{r}\sum_{t}A_{n,t,r} \quad \forall n \in N $
 
### Turno en día sin importar el rol
- Restricción auxiliar para contar día en turno en cualquier rol

$B_{n,t} = \displaystyle\sum_{r}A_{n,t,r} \quad \forall n \in N, \space \forall t \in T$
### Mínimo número de trabajadores por día
- Restricción del mínimo de trabajadores por día

$\displaystyle\sum_{n} A_{n,t,r} \ge \omega_r \quad \forall t \in T \quad \forall r \in R $

### Mínimo valor de experiencia por día
- Restricción del mínimo de experiencia por día

$\displaystyle\sum_{n} A_{n,t,r} \cdot \nu_{n,r} \ge \tau_r \quad \forall t \in T \quad \forall r \in R$


### Condición de inicio/finalización de turno
- Restricción auxiliar para marcar el inicio de turno

$Y_{n,t,r} - Z_{n,t,r} = A_{n,t-1,r} - A_{n,t,r} \quad \forall n \in N, \space \forall t \in T \quad \forall r $

### No simultaneidad de estados de turno
- Restricción auxiliar para evitar que tanto el final y el inicio de turno se den simultaneamente

$Y_{n,t,r} + Z_{n,t,r} \leq 1 \quad \forall n \in N, \space \forall t \in T, \forall r $

### No simultaneidad de estados de rol
- Restricción auxiliar para evitar que un trabajador tenga simultaneamente varios roles

$\displaystyle\sum_{r} A_{n,t,r} \leq 1  \quad \forall n \in N, \space \forall t \in T$

### Mínimo número de días consecutivos en turno
- Restricción de $k$ turnos continuos
  
$\displaystyle\sum_{\rho=0 \space|\space t+\rho \space \leq\space D }^{k-1} A_{n,t+\rho,r} \geq k \cdot Z_{n,t,r} \quad \forall n \in N, \space \forall t \in T, \space \forall r $



### Cantidad mínima de días fuera de turno
- Restricción de $h$ dias de descanso despues de turnos continuos

$\displaystyle\sum_{\rho=0 \space|\space t+\rho \space \leq\space D }^{h-1} B_{n,t+\rho,r} \leq h \cdot (1 -Y_{n,t,r}) \quad \forall n \in N, \space \forall t \in T $

### Continuidad del turno
- Restricción de a lo sumo $c$ cambios en las personas asignadas a turno

$\displaystyle\sum_{n} Z_{n,t,r} \le c_r \quad \forall t \in T \space \forall r $


### Fines de semana
- Restricción de turno continuo en fines de semana

$B_{n,t} = B_{n,t+1} \quad \forall n \in N, \space \forall t \in T \space|\space t = Sabado $ 

### No se trabajan 2 fines de semana consecutivos
- Restricción para limitar asignaciones en fines de semana
  
$B_{n,t} + B_{n,t+7} <= 1 \quad \forall n \in N, \space \forall t \in T \space|\space t = Sabado $ 


### Optimizar la retención de experiencia para realizar turno
- Restricción suave para asegurar que cada trabajador realice un turno por lo menos una vez cada mes

$\displaystyle\sum_{t=1}^{D} A_{n,t,r}\geq 1 - P_{n,r}  \quad \forall n \in N$

### Si trabaja un domingo tiene compensatorio en semana en los 15 dias siguientes
$\displaystyle\sum_{\rho=1 \space|\space t+\rho \space \leq\space D } B_{n,t+\rho} \leq 15 - (3 \cdot B_{n,t}) \quad \forall n \in N, \space \forall t \in T \space | \space t = Domingo $