
#import sys
import numpy as np
import PIL as pl
import os

def DeckCreator(TargetPath, 
                SavePath,
                Black = 'C:\\Users\\Ignacio\\Pictures\\Cartas\\Black.jpg',
                deck_name = 'Deck',
                N_Row = 7,
                N_Column = 10,
                Card_Shape = [300,419]):

    # Parametros iniciales
    N_Cards = N_Row*N_Column
    Card_Shape = tuple(Card_Shape)
    Row_Shape = (Card_Shape[0]*N_Column,Card_Shape[1])
    
    # Hago una lista de los archivos en la ruta
    files = [f for f in os.listdir(TargetPath) if
                f.find(deck_name)<0 and  # No es un deck antiguo
                f.find('.jpg')>=0]       # Es un archivo de imagen

    # Le añado a cada archivo su ruta
    files = list(map(lambda x: TargetPath + x , files))
    
    n_temp = len(files)
    # Rellena con negros hasta el 70 final
    if (n_temp%(N_Cards)) > 0:

        if  n_temp==1:
            files.append(Black)
        while (len(files))%(N_Cards) !=0:

            files.append(Black)
            
        
    # Crea las imagenes fila a fila
    Row_File = []
    for i in range(int(np.ceil(len(files)/N_Column))):
        
        # Escojo las imagenes en sets de N_Column elementos
        Row = [s for s in files[i*N_Column:(i+1)*N_Column] ]
        
        # Extraigo como arrays RGB las imagenes
        imgs_Row = [ pl.Image.open(i).convert('RGB') for i in Row ]
        
        # Las uno horizontalmente
        imgs_comb = np.hstack( (np.asarray( i.resize(Card_Shape) ) for i in imgs_Row ) )
        imgs_comb = pl.Image.fromarray( imgs_comb)  
        
        # Me guardo el nombre del archivo para luego y guardo
        Row_File.append(TargetPath+deck_name+'_'+str(i)+'_temp.jpg')
        imgs_comb.save(TargetPath+deck_name+'_'+str(i)+'_temp.jpg')
    
    # Ahora coge cada N_Rows filas y las une para hacer el cuadrado por columnas
    for i in range(int(len(Row_File)/N_Row)):
        
        # Escojo las filas en sets de N_Row elementos
        Column = [s for s in Row_File[i*N_Row:(i+1)*N_Row] ]
        
        # Extraigo como arrays RGB las imagenes
        imgs_Column = [ pl.Image.open(i).convert('RGB') for i in Column ]
        
        # Las uno verticalmente
        imgs_comb = np.vstack( (np.asarray( i.resize(Row_Shape) ) for i in imgs_Column ) )
        imgs_comb = pl.Image.fromarray( imgs_comb)
        
        # Guardo el resultado
        imgs_comb.save( SavePath+deck_name+'_'+str(i)+'.jpg' )
        
    #Borramos los archivos auxsiliares
    for x in Row_File:
        os.remove(x)
