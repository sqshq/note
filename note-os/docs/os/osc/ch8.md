### **Operating System Concepts 8 - DeadLocks**

### 1 System Model
### 2 Deadlock in Multithreaded Applications
#### Livelock

Threads in deadlock will block indefinitely because each is waiting on the other, while threads in **livelock** can continue execution but make no meaningful progress.


```C
/* thread one runs in this function */ 
void *do work one(void *param) { int done = 0;
    while (!done) {
        pthread_mutex_lock(&first mutex); 
        if (pthread_mutex_trylock(&second mutex)) { 
            /** * Do some work */ 
            pthread_mutex_unlock(&second mutex);
            pthread_mutex_unlock(&first mutex); done = 1; 
        } else 
            pthread_mutex_unlock(&first mutex);
    }
    pthread exit(0);
}

/* thread two runs in this function */ 
void *do_work_two(void *param) { 
int done = 0;
    while (!done) {
        pthread_mutex_lock(&second mutex); 
        if (pthread_mutex_trylock(&first mutex)) {
             /** * Do some work */ p
             thread_mutex_unlock(&first mutex); 
             pthread_mutex_unlock(&second mutex); 
             done = 1; 
         } else 
            pthread_mutex_unlock(&second mutex);
    }
    pthread_exit(0);
}
```
### 3 Deadlock Characterization
#### Necessary Conditions
#### Resource-Allocation Graph
### 4 Methods for Handling Deadlocks

### 5 Deadlock Prevention
#### Mutual Exclusion
#### Hold and Wait
#### No Preemption
#### Circular Wait
### 6 Deadlock Avoidance
#### Safe State
#### Resource-Allocation-Graph Algorithm
#### Banker's Algorithm
### 7 Deadlock Detection
#### Single Instance of Each Resource Type
#### Several Instances of a Resource Type
#### Detection-Algorithm Usage
### 8 Recovery from Deadlock
#### Process and Thread Termination
#### Resource Preemption
