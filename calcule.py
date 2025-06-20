import numpy as np
import scipy.stats as sst
import matplotlib.pyplot as plt
import csv
from matplotlib.widgets import Button, Slider
from matplotlib import cm

def data_recup(name_file):
    file = open(name_file, "r")
    file_data =  file.read()
    file.close()
    file_data = file_data.replace(",",".")
    file_data = file_data.split("\n")
    uncoded_variable = []
    for i in range(len(file_data)):
        uncoded_variable.append(file_data[i].split(";"))
        for a in range(len(uncoded_variable[i])):
            uncoded_variable[i][a] = float(uncoded_variable[i][a])
    uncoded_variable = np.array(uncoded_variable)
    uncoded_result = uncoded_variable[:,(np.shape(uncoded_variable)[1]-1):]
    uncoded_variable = uncoded_variable[:,:(np.shape(uncoded_variable)[1]-1)]
    return uncoded_variable, uncoded_result

def matrix_coding(matrix):
    coded_matrix = matrix
    shape = np.shape(matrix)
    coding_matrix = np.zeros((4,shape[1]))
    for i in range(shape[1]):
        coding_matrix[0,i] = np.max(matrix[:,i]) # max
        coding_matrix[1,i] = np.min(matrix[:,i]) # min
        coding_matrix[2,i] = (coding_matrix[1,i]+ coding_matrix[0,i])/2 # mean
        coding_matrix[3,i] =  coding_matrix[0,i]- coding_matrix[2,i] # step
        for a in range(shape[0]):
            coded_matrix[a,i] = (coded_matrix[a,i] - coding_matrix[2,i])/coding_matrix[3,i]
    return(coded_matrix,coding_matrix)

def matrix_X(matrix):
    coded_variable = matrix_coding(matrix)[0]
    shape = np.shape(coded_variable)
    num_a = int((shape[1]**2+3*shape[1]+2)/2)
    X1 = np.zeros((shape[0],num_a))
    label = []
    for i in range(shape[0]):
        a1 = 0
        a2 = 0
        a3 = 0
        for a in range(num_a):
            if a == 0:
                X1[i,a] = 1
                a1 +=1
                a2 +=1
                label.append("a0")
            elif a3 == 1:
                X1[i,a] = coded_variable[i,a1-1]*coded_variable[i,a1-1]
                label.append("a"+str(a1)+str(a2))
                a3 =0
                a2 +=1
            elif a2 == a1:
                X1[i,a] = coded_variable[i,a1-1]
                label.append("a"+str(a1))
                a3 +=1
            elif a2 == shape[1]:
                X1[i,a] = coded_variable[i,a2-1]*coded_variable[i,a1-1]
                label.append("a"+str(a1)+str(a2))
                a1 += 1
                a2 = a1
            else:
                X1[i,a] = coded_variable[i,a2-1]*coded_variable[i,a1-1]
                label.append("a"+str(a1)+str(a2))
                a2 +=1
    return X1,label[:num_a]

def information_matrix(matrix):
    X1 = matrix_X(matrix)[0]
    X = np.dot(np.transpose(X1),X1)
    return np.linalg.inv(X)

def visuel_info_matrix(X1):
    fig, ax = plt.subplots()
    im = ax.imshow(X1)
    ax.set_title('Pan on the colorbar to shift the color mapping\n'
             'Zoom on the colorbar to scale the color mapping')
    fig.colorbar(im, ax=ax, label='Interactive colorbar')
    plt.show()

def model(matrix,result_matrix):
    X1 = matrix_X(matrix)[0]
    return np.matmul(np.linalg.inv(np.matmul(np.transpose(X1),X1)),np.matmul(np.transpose(X1),result_matrix))

def distance(matrix):
    X = matrix_coding(matrix)[0]
    shape1 = np.shape(X)
    distance_relative_total = []
    for i in range(shape1[0]):
        distance_relative_total.append(np.sqrt(np.sum(np.square(np.full(shape1,X[i]) - X),axis=1)))
    return distance_relative_total    
            
def point_repeter(matrix,valeur):
    matrix_distance = distance(matrix)
    shape = np.shape(matrix_distance)
    distance_moyenne = (np.sum(np.sum(matrix_distance,axis=1))/(shape[0]*shape[1]))
    L = []
    for i in range(shape[0]):
        for a in range(i+1,shape[0]):
            if matrix_distance[i][a] <= distance_moyenne*valeur:
                L.append([i,a])
    index_rep = []
    while L != []:
        index_rep.insert(0,L.pop(0))
        a = 0
        b = 0
        while a != len(L) :
            b = 0
            if len(L)==0:
                a = -1
            elif len(L) > a:
                couple_etu = L[a]
                for i in range(len(index_rep[0])):
                    if index_rep[0][i] == couple_etu[0] and (couple_etu[1] not in index_rep[0]) and len(L) > a:
                        index_rep[0].append(L.pop(a)[1])
                        b = 1
                    elif index_rep[0][i] == couple_etu[1] and (couple_etu[0] not in index_rep[0]) and len(L) > a:
                        index_rep[0].append(L.pop(a)[0])
                        b = 1
                    elif (index_rep[0][i] == couple_etu[1] or index_rep[0][i] == couple_etu[0]) and len(L) > a:
                        b = 1
                        L.pop(a)[0]
                if b == 1:
                    a = 0                   
                else :
                    a+=1 
    return index_rep,distance_moyenne


def best_rep(matrix,valeur):
    index_rep, distence_moy = point_repeter(matrix,valeur)
    matrix_distance = distance(matrix)
    best = [[],distence_moy]
    for i in range(len(index_rep)):
        sum = 0
        tot = 0
        for a in range(len(index_rep[i])):
            for y in range(a+1,len(index_rep[i])):
                sum += matrix_distance[index_rep[i][y]][index_rep[i][a]]
                tot += 1
        if sum/tot <= best[1]:
            best = [index_rep[i],sum/tot]
    return best

def estimation_statistique_simple(X,Y,alpha,valeur):
    model1 = model(X,Y)
    Xcoded,label1 = matrix_X(X)
    shape = np.shape(Xcoded)
    Lrep = best_rep(X,valeur)[0]
    DOFfit = len(Xcoded)-len(model1)-len(Lrep)+1
    DOFexp = len(Lrep)-1
    DOFres = DOFexp+DOFfit
    Ym = []
    for i in range(len(Lrep)):
        Ym.append(Y[Lrep[i]])
    Ys = np.dot(Xcoded,model1)    
    Ym = np.full(shape[0],np.average(Ym))
    Ys = np.reshape(Ys,(len(Ys),1))
    Ym = np.reshape(Ym,(len(Ym),1))
    Sfit = np.sum(np.square(Ys - Ym))/DOFfit
    Sexp = np.sum(np.square(Y - Ym))/DOFexp
    Sres = np.sum(np.square(Ys - Y))/DOFres
    student = sst.t.ppf(1 - alpha/2,DOFres)
    Xinfo = np.diagonal(information_matrix(X))
    Cli = np.transpose((np.sqrt(Xinfo*Sres))*student)
    model1 = np.ndarray.tolist(np.reshape(model1,(len(model1),1)))
    Cli = np.ndarray.tolist(np.reshape(Cli,(len(Cli),1)))
    matrix_export = []
    for i in range(len(label1)):
        matrix_export.append([label1[i],model1[i][0],Cli[i][0]])
    info_export = (DOFfit,DOFexp,DOFres,Sfit,Sexp,Sres,student)
    return model1,matrix_export,info_export

def generation_a(variable):
    num_var = len(variable)
    lvar = []
    a1 = 0
    a2 = 0
    for i in range(int((num_var**2+3*num_var+2)/2)):
        if i == 0:
            lvar.append(1)
        elif a2 == 0:
            lvar.append(variable[a1])
            a2 += 1
        elif a2 == num_var-1:
            lvar.append(variable[a1]*variable[a2])
            a1 += 1
            a2 = 0
        else:
            lvar.append(variable[a1]*variable[a2])
            a2 +=1
    return lvar


def f(model1,variable):
    mat_a = generation_a(variable)
    total = 0
    for i in range(len(mat_a)):
        total += model1[i][0]*mat_a[i]
    return total

def ANOVA_test(f_statistic, alpha, df_numerator, df_denominator):
    f_critique = sst.f.ppf(1 - alpha, df_numerator, df_denominator)
    print(f_critique)
    # Test de validité
    if f_statistic <= f_critique:
        return "Model is valid"
    else:
        return "Model is not valid"





