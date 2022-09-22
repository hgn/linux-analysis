# Mass Retirement


```
    104a:	    nopw   0x0(%rax,%rax,1)
    1050:	/-> inc    %r8
    1053:	|   inc    %r9
    1056:	|   inc    %r10
    1059:	|   inc    %r11
    105c:	|   inc    %r12
    105f:	|   inc    %r13
    1062:	|   inc    %r14
    1065:	|   inc    %r15
    1068:	|   sub    $0x1,%rax
    106c:	\-- jne    1050 <main+0x10>
    106e:	    xor    %eax,%eax
    1070:	    ret
```


```
$ perf stat -C 3 -e cycles,uops_executed.core,uops_dispatched_port.port_0,uops_dispatched_port.port_1,uops_dispatched_port.port_2,uops_dispatched_port.port_3,uops_dispatched_port.port_4,uops_dispatched_port.port_5,uops_dispatched_port.port_6,uops_dispatched_port.port_7 -- taskset -c 3 ./mass-retirement

 Performance counter stats for 'CPU(s) 3':

    23.446.408.180      cycles                                                               (49,98%)
    90.163.481.726      uops_executed.core                                                   (50,04%)
    21.389.175.150      uops_dispatched_port.port_0                                          (50,06%)
    22.606.476.356      uops_dispatched_port.port_1                                          (50,06%)
         3.668.423      uops_dispatched_port.port_2                                          (50,06%)
         3.551.109      uops_dispatched_port.port_3                                          (39,97%)
         3.425.040      uops_dispatched_port.port_4                                          (39,96%)
    22.732.252.823      uops_dispatched_port.port_5                                          (39,95%)
    23.322.174.259      uops_dispatched_port.port_6                                          (39,96%)
         1.709.310      uops_dispatched_port.port_7                                          (39,95%)

       6,006952658 seconds time elapsed
```

```
perf stat -B --topdown -C 3 -- taskset -c 3 ./mass-retirement

 Performance counter stats for 'CPU(s) 3':

                                    retiring      bad speculation       frontend bound        backend bound
S0-D0-C3           1               191,6%                 0,1%                 7,3%               -99,0%

       6,021851103 seconds time elapsed
```


