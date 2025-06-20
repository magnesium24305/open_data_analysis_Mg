from calcule import*
import matplotlib.pyplot as plt



def update(val):
    global cbar,model1
    cbar.remove()
    for i in range(num_var-2):
        lvar_ini[i+2] = list_slider[i+2].val
    ax.cla()
    pcol = ax.pcolormesh(var1,var2, f(model1,lvar_ini))
    cbar = plt.colorbar(pcol)

def graph(model):
    global ax,fig,var1,var2,lvar_ini,num_var,list_slider,cbar,model1
    model1 = model
    num_var = int((-3/2) + (1/2)*np.sqrt(1+8*len(model1)))
    lvar_ini = []
    var1,var2 = np.meshgrid(np.linspace(-1,1,1000),np.linspace(-1,1,1000))
    lvar_ini = [var1,var2]
    for i in range(num_var-2):
        lvar_ini.append(0)
    fig, ax = plt.subplots()
    pcol = ax.pcolormesh(var1,var2, f(model1,lvar_ini))
    cbar = plt.colorbar(pcol)
    ax.set_xlabel("variable 1")
    ax.set_ylabel("variable 2")
    fig.subplots_adjust( bottom = num_var*0.05)
    list_axes_slider = []
    list_slider = [var1,var2]
    for i in range(num_var-2):
        list_axes_slider.append(fig.add_axes([0.15, 0.02+0.05*i, 0.65, 0.03]))
        list_slider.append( Slider(
            ax=list_axes_slider[i],
            label="varible " + str(i+3),
            valmin=-1,
            valmax=1,
            valinit=lvar_ini[i+2],
        ))
    
    for i in range(num_var-2):
        list_slider[i+2].on_changed(update)
   
    plt.show()



