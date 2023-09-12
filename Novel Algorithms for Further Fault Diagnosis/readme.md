### Project code structure

In order to write and run the project better and reduce code redundancy, the project structure is mainly divided into the following several parts.

```
new-code
--- Algorithm: Some new algorithms' modules can be written directly into it, which is responsible for finding a fault-free vertex in H after generating a network.
--- experiment_result: file folder to record experimental results
--- network: file folder in which modules of network are
--- Node: the composition of nodes in the network
--- paper_start: the main file which integrates the modules of algorithm, network and node and we officially start our simulation and set the parameters here.
--- utils: file folder in which we put some small tools such as indicator calculation and other functions
```

> In the paper_start folder, the logic of a main file is:
>
> 1. Set parameters related to the generated network, including:
>
> - number of loops
> - Some parameters of the network, the value of g for g-good-neighbor property, the degree of each vertex, etc
>
> 2. The combination of these parameters will be placed in a parameter list for code analysis. Each group of parameters, such as [number of loops, number of An nodes, ...]
> 3. Import network module, initialize the network through this set of parameters, and obtain the variable network
> 4. Pass network to the algorithm Algorithm to be diagnosed, perform diagnosis, and the result of diagnosis is to return a faultless H vertex
> 5. Print relevant parameters and data
> 6. After finding a faultless H vertex, call the PMC algorithm in utils for quick diagnosis
> 7. Print relevant parameters and data
> 8. When PMC model cannot find the any new H faultless vertex and the entire subnetwork H has not been diagnosed, the algorithm is called for the second time to perform diagnosis, and the PMC process continues until all accessible vertices in H are diagnosed.
