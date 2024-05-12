import sys
import os
import networkx as nx
from itertools import combinations

variable_to_numeric = {}
numeric_counter = 0  


def init_var(no_nodes,k1,k2):
   global numeric_counter
   for i in range(1, no_nodes + 1):
       numeric_counter += 1
       variable_to_numeric[f'X_{i}'] = numeric_counter
       

   for i in range(1, no_nodes + 1):
       numeric_counter += 1
       variable_to_numeric[f'Y_{i}'] = numeric_counter

def create_imply_cnf2(cand_nod,G,k,k1,k2):
    if k==k1:
            uniq_var='X'
    else :
            uniq_var='Y'
    neighbours = [n for n in G.neighbors(cand_nod) if G.degree(n)>=k-1]
    subgraph = G.subgraph([cand_nod]+neighbours)
    subgraph_eligibal_nodes= [n for n in subgraph.neighbors(cand_nod) if subgraph.degree(n)>=k-1]
    rhs = str(f'~{uniq_var}_{cand_nod}')
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
              conjunctions.append(str(f'{uniq_var}_{adj_node}'))
          else:
              conjunctions.append(str(f'~{uniq_var}_{adj_node}'))
       perm_list.append(conjunctions)
       i+=1
    for perm in perm_list:
        var_list=factor_list
        comp_list=[]
        for var in perm:
            for i,_ in enumerate(var_list):
                if var in var_list[i]:
                    comp_list.append(var_list[i])
                elif (str(f"~{var}") in var_list[i]) or (str(f"{var}").strip("~").strip(" ") in var_list[i]):
                    continue
                else:
                    comp_list.append(var_list[i]+[var])
        factor_list=comp_list
    
    cnf_list=[]
    for factor in factor_list:
        var_str="|".join(factor)
        cnf_list.append(str(f"({var_str})"))
    for eln in non_eligibal_neighbour:
        cnf_list.append(str(f"(~{uniq_var}_{cand_nod}|~{uniq_var}_{eln})"))
    print(len(cnf_list))
    #if k==5:
      #  print(cnf_list)
    return cnf_list

def create_card_const(node_deg_map,k1,k2):
    const_list=[]
    for k,k_deg_nodes in node_deg_map.items():
        if k==k1:
            uniq_var='X'
        else :
            uniq_var='Y'
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
    of.close()

def get_cnf(G,k1,k2,graph_file):
         cnf_clauses=[]
         node_deg_map={}
         cand_node_k1 = []
         cand_node_k2 = []
         for cand_nod in list(G.nodes):
             subK1 = G.subgraph([cand_nod ] + [n for n in G.neighbors(cand_nod) if G.degree(n)>=k1-1])
             subK2 = G.subgraph([cand_nod ] + [n for n in G.neighbors(cand_nod) if G.degree(n)>=k2-1])
             if len([node for (node,val) in subK1.degree() if val>=k1-1])>=k1:
                 cand_node_k1.append(cand_nod)
             if len([node for (node,val) in subK2.degree() if val>=k2-1])>=k2:
                 cand_node_k2.append(cand_nod)
         node_deg_map[k1]=cand_node_k1
         node_deg_map[k2]=cand_node_k2
         for cand_nod in list(G.nodes):
            print(f" for node {cand_nod} \n")
            cnf_clauses.append(f'(X_{cand_nod} | Y_{cand_nod})')
            cnf_clauses.append(f'(~X_{cand_nod} | ~Y_{cand_nod})')
            #clause_list=[]
            for k in [k1,k2]:
               if k==k1:
                  uniq_var='X'
                  cand_nodes=cand_node_k1
               else :
                  uniq_var='Y' 
                  cand_nodes=cand_node_k2
               print(f" for k {k} \n")
               if cand_nod in cand_nodes:
                   #print("hey")
                   cnf_clauses+=create_imply_cnf2(cand_nod,G,k,k1,k2)
         cnf_clauses+=create_card_const(node_deg_map,k1,k2)
         for all_nod in list(G.nodes):
             if(all_nod not in cand_node_k1):
                 cnf_clauses.append(f'(~X_{all_nod})')
             if(all_nod not in cand_node_k2):
                 cnf_clauses.append(f'(~Y_{all_nod})')
         #print(cnf_clauses)
       #  convert_2_DIMAC
         convert_2_dimac(f'{graph_file}.satinput',cnf_clauses)
    

def compute_problem(graph_file):

    gf = open(f"{graph_file}.graphs","r")
    lines = gf.readlines()
    num_lines = len(lines)
    x = lines[0].strip().split(' ')
    no_nodes=int(x[0])
    no_edges=int(x[1])
    k1=int(x[2])
    k2=int(x[3])
    G = nx.Graph()
    #for i in range(1,no_nodes+1):
    #	G.add_node(i)
    for i in range(1,no_edges+1):
        u = lines[i].strip().split(' ')[0]
        v = lines[i].strip().split(' ')[1]
        G.add_edge(u,v)
    init_var(no_nodes,k1,k2)
    get_cnf(G,k1,k2,graph_file)
    gf.close()

def compute_out(file_name):
    rs = open(f'{file_name}.satoutput',"r")
    lines = rs.readlines()
    mp = open(f'{file_name}.mapping','w')
    gf = open(f'{file_name}.graphs',"r")
    gf_lines = gf.readlines()
    num_gf_lines = len(gf_lines)
    x = gf_lines[0].strip().split(' ')
    no_nodes=int(x[0])
    no_edges=int(x[1])
    k1=int(x[2])
    k2=int(x[3])
    G = nx.Graph()
    for i in range(1,no_edges+1):
        u = gf_lines[i].strip().split(' ')[0]
        v = gf_lines[i].strip().split(' ')[1]
        G.add_edge(u,v)
    numeric_to_node_map={"1":[],"2":[]}
    no_v=len(list(G.nodes))
    if(lines[0].strip("\n")=="SAT"):
       result_list=lines[1].strip("\n").strip("0").strip(" ").split(" ")
      # print(result_list)
       for el in result_list:
           if int(el)<0:
               continue
           elif int(el)<no_v+1 and int(el)>0:
               numeric_to_node_map["1"].append(el)
           elif int(el)>no_v and int(el)>0:
               numeric_to_node_map["2"].append(str(int(el)-no_v))
       mp.write('#1 \n')
       print('#1 \n')
       mp.write(" ".join(numeric_to_node_map["1"]) + '\n')
       print(" ".join(numeric_to_node_map["1"]) + '\n')
       mp.write('#2 \n')
       print('#2 \n')
       mp.write(" ".join(numeric_to_node_map["2"]) + '\n')
       print(" ".join(numeric_to_node_map["2"]) + '\n')
    else :
        mp.write('0 \n')
    mp.close()
    gf.close()
    rs.close()

if __name__=='__main__':

    #compute_problem("test")
    #exit(0)
    #sys.argv[1]='3'

    if sys.argv[1]=='1':
       if not(os.path.isfile(sys.argv[2]+".graphs")):
          print("ERROR: Input Graph File does not exist")
          sys.exit(1)
       compute_problem(sys.argv[2])
    if sys.argv[1]=='2':
       if not(os.path.isfile(sys.argv[2]+".satoutput")):
          print("ERROR: Input sat File does not exist")
          sys.exit(1)
       if not(os.path.isfile(sys.argv[2]+".graphs")):
          print("ERROR: Input graph File does not exist")
          sys.exit(1)
       compute_out(sys.argv[2])
    #if not(os.path.isfile(sys.argv[2])):
    #	print("ERROR: Output Subgraph File does not exist")
    #	sys.exit(1)
  #  if sys.argv[2]=='1':
       
    #if sys.argv[3]=='2': 
    #	compute_problem2(sys.argv[1], sys.argv[2])
    #if sys.argv[2]!='1' and sys.argv[2]!='2':
     #   print("Check the arguments carefully")