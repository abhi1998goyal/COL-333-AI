import sys
import os
import networkx as nx
from itertools import combinations
import subprocess

variable_to_numeric = {}
numeric_counter = 0  


def init_var(no_nodes):
   global numeric_counter
   for i in range(1, no_nodes + 1):
       numeric_counter += 1
       variable_to_numeric[f'X_{i}'] = numeric_counter


def create_card_const(node_deg_map,k1):
    const_list=[]
    for k,k_deg_nodes in node_deg_map.items():
        if k==k1:
            uniq_var='X'
        for i in range(0,len(k_deg_nodes)+1):
            if i!=k:
                combo_k = list(combinations(k_deg_nodes,i))
                if combo_k:
                    for j in range(0,len(combo_k)):
                        perm=[]
                        for node in k_deg_nodes:
                            if(node in combo_k[j]):
                                perm.append(f'~{uniq_var}_{node}')
                            else :
                                perm.append(f'{uniq_var}_{node}')
                        const_list.append("("+"|".join(perm)+")")
            else:
                continue
    return const_list

def convert_2_dimac(outFile,cnf_clauses):
    of = open(outFile,'w')
    of.write('p cnf %d %d\n' %(numeric_counter, len(cnf_clauses)))
    for cls in cnf_clauses:
        var_list=cls.strip(" ").strip("(").strip(")").strip(" ").split("|")
        for var in var_list:
            if var.strip(" ")[0]=="~":
                of.write(f'-{variable_to_numeric[var.strip(" ").strip("~")]} ')
            else :
                of.write(f'{variable_to_numeric[var.strip(" ").strip("~")]} ')
        of.write("0 \n")

def get_cnf(G,k1,graph_file):
         cnf_clauses=[]
         node_deg_map={}
         cand_node_k1=[]
         for cand_nod in list(G.nodes):
             subK1 = G.subgraph([cand_nod ] + [n for n in G.neighbors(cand_nod) if G.degree(n)>=k1-1])
             if len([node for (node,val) in subK1.degree() if val>=k1-1])>=k1:
                 cand_node_k1.append(cand_nod)
         node_deg_map[k1]=cand_node_k1
         for cand_nod in list(G.nodes):
            print(f" for node {cand_nod} \n")
            for k in [k1]:
               if k==k1:
                  uniq_var='X'
                  cand_nodes=cand_node_k1
              # print(f" for k {k} \n")
               if cand_nod in cand_nodes:
                 #  print("hey")
                  cnf_clauses+=create_imply_cnf2(cand_nod,G,k)
         cnf_clauses+=create_card_const(node_deg_map,k1)
         for all_nod in list(G.nodes):
             if(all_nod not in cand_node_k1):
                 cnf_clauses.append(f'(~X_{all_nod})')
         #print(cnf_clauses)
       #  convert_2_DIMAC
         convert_2_dimac(f'{graph_file}.best',cnf_clauses)

def create_imply_cnf2(cand_nod,G,k):
    neighbours = [n for n in G.neighbors(cand_nod) if G.degree(n)>=k-1]
    subgraph = G.subgraph([cand_nod]+neighbours)
    subgraph_eligibal_nodes= [n for n in subgraph.neighbors(cand_nod) if subgraph.degree(n)>=k-1]
    rhs = str(f'~X_{cand_nod}')
    combo = list(combinations(subgraph_eligibal_nodes,k-1))
    non_eligibal_neighbour=[n for n in neighbours if n not in subgraph_eligibal_nodes]
    len_combo=len(combo)
    i=0
    perm_list=[]
    factor_list=[[rhs]]
    while i<len_combo:
       conjunctions=[]
       for adj_node in neighbours:
          if(adj_node in combo[i]):
              conjunctions.append(str(f'X_{adj_node}'))
          else:
              conjunctions.append(str(f'~X_{adj_node}'))
       perm_list.append(conjunctions)
       i+=1
    for perm in perm_list:
        var_list=factor_list
        comp_list=[]
        for var in perm:
            for i,_ in enumerate(var_list):
                if var in var_list[i]:
                    comp_list.append(var_list[i])
                elif str(f"~{var}") in var_list[i] or (str(f"{var}").strip("~").strip(" ") in var_list[i]):
                    continue
                else:
                    comp_list.append(var_list[i]+[var])
        factor_list=comp_list
    
    cnf_list=[]
    for factor in factor_list:
        var_str="|".join(factor)
        cnf_list.append(str(f"({var_str})"))
    for eln in non_eligibal_neighbour:
        cnf_list.append(str(f"(~X_{cand_nod}|~X_{eln})"))
    #print(len(cnf_list))
    #if k==5:
      #  print(cnf_list)
    return cnf_list
    

def compute_problem(graph_file):

    gf = open(graph_file,"r")
    lines = gf.readlines()
    num_lines = len(lines)
    x = lines[0].strip().split(' ')
    no_nodes=int(x[0])
    no_edges=int(x[1])
    k1=int(x[2])
    G = nx.Graph()
    #for i in range(1,no_nodes+1):
    #	G.add_node(i)
    for i in range(1,no_edges+1):
        u = lines[i].strip().split(' ')[0]
        v = lines[i].strip().split(' ')[1]
        G.add_edge(u,v)
    nx.draw(G, with_labels = True)
    plt.savefig("plot.png")
    init_var(no_nodes,k1)
    get_cnf(G,k1)

def compute_best(graph_file):

    gf = open(graph_file+".graphs","r")
    lines = gf.readlines()
    num_lines = len(lines)
    x = lines[0].strip().split(' ')
    no_nodes=int(x[0])
    no_edges=int(x[1])
    G = nx.Graph()
    for i in range(1,no_edges+1):
        u = lines[i].strip().split(' ')[0]
        v = lines[i].strip().split(' ')[1]
        G.add_edge(u,v)

    node_degree_map=dict(G.degree())
    sorted_deg_map= dict(sorted(node_degree_map.items(),key=lambda x:x[1],reverse=True))
    bkey,bval= list(sorted_deg_map.items())[0]
    k1=bval+1
    for index, (key, val) in enumerate(sorted_deg_map.items()):
        if val<=index:
            k1=val+1
            break
        else :
            if index<len(sorted_deg_map)-1:
               next_key, next_val = list(sorted_deg_map.items())[index + 1]
               if index>next_val and val>next_val:
                  k1=index+1
                  break
            
    #for i in range(1,no_nodes+1):
    #	G.add_node(i)
    init_var(no_nodes)
    best_k =1
    k_list=[i for i in range(k1,0,-1)]
    left=0
    right=len(k_list)-1
    result_list=[]
    res_file_name=str(f"{graph_file}.mapping")
    while(left<=right):
        pdel = subprocess.Popen(("rm",res_file_name), stdout=subprocess.PIPE)
        pdel.wait()
        mid = (left + right)//2
        get_cnf(G,k_list[mid],graph_file)
        inp_fl=str(f"{graph_file}.best")
        out_fl=str(f"{graph_file}.bestout")
        args = ("./minisat", inp_fl, out_fl)
        popen = subprocess.Popen(args, stdout=subprocess.PIPE)
        popen.wait()
        rs = open(out_fl,"r")
        lines = rs.readlines()
        if(lines[0].strip("\n")=="SAT"):
           result_list=lines[1].strip("\n").strip("0").strip(" ").split(" ")
           if k_list[mid]>best_k:
             pos_res = list(filter(lambda x: int(x) >0, result_list))
             ro=open(res_file_name,"w")
             ro.write('#1 \n')
             ro.write(" ".join(pos_res) + '\n')
             best_k=k_list[mid]
           right=mid-1
        else:
           left=mid+1
        print(f"ran for {k_list[mid]} \n")
    print(best_k)

   

if __name__=='__main__':

    compute_best(sys.argv[1])

