import dictionary
import math
import os
from fpdf import FPDF


FPath = os.path.dirname(os.path.abspath(__file__))


def calculeaza_media_aritmetica(verbose=False):
    # Calculeaza media aritmetica a fiecarui caracter pentru fiecare genom
    #Ma = sum(a1 + a2+...an)/ n
    media_art_dict = {}
    keys = dictionary.genotipuri.keys()
    for k in keys:
        new_dict = dictionary.genotipuri.get(k)
        second_keys = new_dict.keys()
        caracteristica_dict = {}
        for j in second_keys:
            lista = new_dict.get(j)
            NrMasuratori  = len(lista)
            if(NrMasuratori<5):
                print("Error!")
            # Aduna elementele
            suma = 0
            for i in range(NrMasuratori):
                suma += lista[i]
                media_art = round(suma / NrMasuratori, 2)
            #print(media_art)
            caracteristica_dict.update({j : media_art})
        media_art_dict.update({k : caracteristica_dict})

    if(verbose==True):
        print(media_art_dict)

    return media_art_dict

def calculeaza_varianta(verbose=False):
        # Forumla variantei
        # Calculeaza varianta.
        # S2 = Suma(x - X*)2/ n- 1
        # x* - media aritmetica a caracterului respectiv
        varianta_dictionar_l1 = {}
        default_dictionary = calculeaza_media_aritmetica(False)
        keys_general = dictionary.genotipuri.keys()
        keys_mediaAritmetica = default_dictionary.keys()

        for k1, k2 in zip(keys_general, keys_mediaAritmetica):
            #print(k1, "+" , k2)
            second_level_k1 = dictionary.genotipuri.get(k1)
            second_level_k2 = default_dictionary.get(k2)
            varianta_dictionar_l2 = {}
            for k1_2, k2_2 in zip(second_level_k1.keys(), second_level_k2.keys()):
                #print(k1_2, "+", k2_2)
                lista_genotipuri = second_level_k1.get(k1_2)
                media = second_level_k2.get(k2_2)
                lista_diferenta = []
                #print(lista_genotipuri, " : " , media, "lungime :" , len(lista_genotipuri))
                for i in lista_genotipuri:
                    diferenta = round(i - media, 3)
                    lista_diferenta.append(diferenta)

                #print(lista_diferenta)
                lista_patrat = []
                for i in lista_diferenta:
                    calcul = round(i**2,3)
                    lista_patrat.append(calcul)
                # Calculeaza suma listei....

                #print(lista_patrat)
                raport = len(lista_patrat) - 1
                suma_listei = round(sum(lista_patrat),2)
                rezultat = round((suma_listei / raport ),2)
                varianta_dictionar_l2.update({k1_2: rezultat})
                #print(rezultat)
            varianta_dictionar_l1.update({k1: varianta_dictionar_l2})

        if(verbose==True):
            print(varianta_dictionar_l1)

        return varianta_dictionar_l1

def calculeaza_abaterea_standard(verbose=False):
    # Calculeaza abaterea standard...
    # Formula pentru abaterea standard este.
    # Radacina patrata din varianta ( sqrt(s2))
    obtine_dictionar = calculeaza_varianta(False)
    keys_dictionar = obtine_dictionar.keys()
    dictionar_abaterea_standar = {}
    #print(keys_dictionar)
    for k in keys_dictionar:
        transpune_dictionar = obtine_dictionar.get(k)
        valori_abaterea_standard = {}
        for j in transpune_dictionar.keys():
            varianta = transpune_dictionar.get(j)
            extrage_radacina = round(math.sqrt(varianta),2)
            valori_abaterea_standard.update({j : extrage_radacina })
        dictionar_abaterea_standar.update({k:valori_abaterea_standard})

    if(verbose==True):
        print(dictionar_abaterea_standar)

    return dictionar_abaterea_standar

def calculeaza_coef_de_variatie(verbose=False):
    # Calculeaza coeficientul de variatie
    # Formula pentru coeficientul de variatie este...
    # s% = ( 100 * s) / x*
    dictionar_abatere = calculeaza_abaterea_standard(False)
    dictionar_media_art = calculeaza_media_aritmetica(False)
    keys_dictionar_abatere = dictionar_abatere.keys()
    keys_dictionar_media_art = dictionar_media_art.keys()
    dictionar_coef_variatie = {}
    #print(dictionar_abatere, dictionar_media_art)
    for k1, k2 in zip(keys_dictionar_abatere, dictionar_media_art):
        second_level_k1 = dictionar_abatere.get(k1)
        second_level_k2 = dictionar_media_art.get(k2)
        coef_variatie = {}
        for k1_2, k2_2 in zip(second_level_k1.keys(), second_level_k2.keys()):
            valoare_abaterea = second_level_k1.get(k1_2)
            valoare_medie = second_level_k2.get(k2_2)
            #print(valoare_abaterea, valoare_medie)
            formula = round((100 * valoare_abaterea) / valoare_medie, 2)
            coef_variatie.update({ k1_2: formula })
        dictionar_coef_variatie.update({k1: coef_variatie})

    if(verbose==True):
        print(dictionar_coef_variatie)

    return dictionar_coef_variatie

def writePDF(filename="rezultate.pdf", verbose=False):
    fpath = os.path.join(FPath, filename)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, 'Media aritmetica', 0, 0, 'C')
    pdf.ln(20)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(20)
    pdf.cell(40,10,"Genotip", 1,0,'C')
    pdf.cell(40,10,"Lungime Spic", 1,0,'C')
    pdf.cell(40,10, "Greutate Boabe", 1,0,'C')
    pdf.cell(40,10, "Numar Boabe Spic",1,0,'C')
    pdf.ln(10)
    pdf.cell(20)


    dictionar_media_art = calculeaza_media_aritmetica(False)
    dictionar_varianta = calculeaza_varianta(False)
    dictionar_abaterea_standar = calculeaza_abaterea_standard(False)
    dictionar_coef_variatie = calculeaza_coef_de_variatie(False)

    keys_dictionar_media_art = dictionar_media_art.keys()
    keys_dictionar_varianta = dictionar_varianta.keys()
    keys_dictionar_abatere = dictionar_abaterea_standar.keys()
    keys_dictionar_coef_variatie  = dictionar_coef_variatie.keys()

    for k1, k2, k3, k4 in zip(keys_dictionar_media_art, keys_dictionar_varianta, keys_dictionar_abatere, keys_dictionar_coef_variatie):
        pdf.cell(40, 10, str(k1), 1,0, 'C')
        second_level_k1 = dictionar_media_art.get(k1)
        second_level_k2 = dictionar_varianta.get(k2)
        second_level_k3 = dictionar_abaterea_standar.get(k3)
        second_level_k4 = dictionar_coef_variatie.get(k4)
        count = 1
        for k1_2, k2_2, k3_2, k4_2 in zip(second_level_k1.keys(), second_level_k2.keys(), second_level_k3.keys(), second_level_k4.keys()):
            media_aritmetica = second_level_k1.get(k1_2)
            varianta = second_level_k2.get(k2_2)
            abaterea = second_level_k3.get(k3_2)
            coef_variatie = second_level_k4.get(k4_2)

            pdf.cell(40, 10, str(media_aritmetica), 1,0, 'C')
            if((count % 3) == 0):
                pdf.ln(10)
                pdf.cell(20)
            count +=1



    pdf.ln(40)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, 'Varianta', 0, 0, 'C')
    pdf.ln(20)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(20)
    pdf.cell(40,10,"Genotip", 1,0,'C')
    pdf.cell(40,10,"Lungime Spic", 1,0,'C')
    pdf.cell(40,10, "Greutate Boabe", 1,0,'C')
    pdf.cell(40,10, "Numar Boabe Spic",1,0,'C')
    pdf.ln(10)
    pdf.cell(20)


    dictionar_media_art = calculeaza_media_aritmetica(False)
    dictionar_varianta = calculeaza_varianta(False)
    dictionar_abaterea_standar = calculeaza_abaterea_standard(False)
    dictionar_coef_variatie = calculeaza_coef_de_variatie(False)

    keys_dictionar_media_art = dictionar_media_art.keys()
    keys_dictionar_varianta = dictionar_varianta.keys()
    keys_dictionar_abatere = dictionar_abaterea_standar.keys()
    keys_dictionar_coef_variatie  = dictionar_coef_variatie.keys()

    for k1, k2, k3, k4 in zip(keys_dictionar_media_art, keys_dictionar_varianta, keys_dictionar_abatere, keys_dictionar_coef_variatie):
        pdf.cell(40, 10, str(k1), 1,0, 'C')
        second_level_k1 = dictionar_media_art.get(k1)
        second_level_k2 = dictionar_varianta.get(k2)
        second_level_k3 = dictionar_abaterea_standar.get(k3)
        second_level_k4 = dictionar_coef_variatie.get(k4)
        count = 1
        for k1_2, k2_2, k3_2, k4_2 in zip(second_level_k1.keys(), second_level_k2.keys(), second_level_k3.keys(), second_level_k4.keys()):
            media_aritmetica = second_level_k1.get(k1_2)
            varianta = second_level_k2.get(k2_2)
            abaterea = second_level_k3.get(k3_2)
            coef_variatie = second_level_k4.get(k4_2)

            pdf.cell(40, 10, str(varianta), 1,0, 'C')
            if((count % 3) == 0):
                pdf.ln(10)
                pdf.cell(20)
            count +=1

    pdf.ln(40)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, 'Abaterea Standard', 0, 0, 'C')
    pdf.ln(20)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(20)
    pdf.cell(40,10,"Genotip", 1,0,'C')
    pdf.cell(40,10,"Lungime Spic", 1,0,'C')
    pdf.cell(40,10, "Greutate Boabe", 1,0,'C')
    pdf.cell(40,10, "Numar Boabe Spic",1,0,'C')
    pdf.ln(10)
    pdf.cell(20)


    dictionar_media_art = calculeaza_media_aritmetica(False)
    dictionar_varianta = calculeaza_varianta(False)
    dictionar_abaterea_standar = calculeaza_abaterea_standard(False)
    dictionar_coef_variatie = calculeaza_coef_de_variatie(False)

    keys_dictionar_media_art = dictionar_media_art.keys()
    keys_dictionar_varianta = dictionar_varianta.keys()
    keys_dictionar_abatere = dictionar_abaterea_standar.keys()
    keys_dictionar_coef_variatie  = dictionar_coef_variatie.keys()

    for k1, k2, k3, k4 in zip(keys_dictionar_media_art, keys_dictionar_varianta, keys_dictionar_abatere, keys_dictionar_coef_variatie):
        pdf.cell(40, 10, str(k1), 1,0, 'C')
        second_level_k1 = dictionar_media_art.get(k1)
        second_level_k2 = dictionar_varianta.get(k2)
        second_level_k3 = dictionar_abaterea_standar.get(k3)
        second_level_k4 = dictionar_coef_variatie.get(k4)
        count = 1
        for k1_2, k2_2, k3_2, k4_2 in zip(second_level_k1.keys(), second_level_k2.keys(), second_level_k3.keys(), second_level_k4.keys()):
            media_aritmetica = second_level_k1.get(k1_2)
            varianta = second_level_k2.get(k2_2)
            abaterea = second_level_k3.get(k3_2)
            coef_variatie = second_level_k4.get(k4_2)

            pdf.cell(40, 10, str(abaterea), 1,0, 'C')
            if((count % 3) == 0):
                pdf.ln(10)
                pdf.cell(20)
            count +=1

    pdf.ln(40)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, 'Coeficientul de variatie', 0, 0, 'C')
    pdf.ln(20)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(20)
    pdf.cell(40,10,"Genotip", 1,0,'C')
    pdf.cell(40,10,"Lungime Spic", 1,0,'C')
    pdf.cell(40,10, "Greutate Boabe", 1,0,'C')
    pdf.cell(40,10, "Numar Boabe Spic",1,0,'C')
    pdf.ln(10)
    pdf.cell(20)


    dictionar_media_art = calculeaza_media_aritmetica(False)
    dictionar_varianta = calculeaza_varianta(False)
    dictionar_abaterea_standar = calculeaza_abaterea_standard(False)
    dictionar_coef_variatie = calculeaza_coef_de_variatie(False)

    keys_dictionar_media_art = dictionar_media_art.keys()
    keys_dictionar_varianta = dictionar_varianta.keys()
    keys_dictionar_abatere = dictionar_abaterea_standar.keys()
    keys_dictionar_coef_variatie  = dictionar_coef_variatie.keys()

    for k1, k2, k3, k4 in zip(keys_dictionar_media_art, keys_dictionar_varianta, keys_dictionar_abatere, keys_dictionar_coef_variatie):
        pdf.cell(40, 10, str(k1), 1,0, 'C')
        second_level_k1 = dictionar_media_art.get(k1)
        second_level_k2 = dictionar_varianta.get(k2)
        second_level_k3 = dictionar_abaterea_standar.get(k3)
        second_level_k4 = dictionar_coef_variatie.get(k4)
        count = 1
        for k1_2, k2_2, k3_2, k4_2 in zip(second_level_k1.keys(), second_level_k2.keys(), second_level_k3.keys(), second_level_k4.keys()):
            media_aritmetica = second_level_k1.get(k1_2)
            varianta = second_level_k2.get(k2_2)
            abaterea = second_level_k3.get(k3_2)
            coef_variatie = second_level_k4.get(k4_2)

            pdf.cell(40, 10, str(str(coef_variatie) +  "%"), 1,0, 'C')
            if((count % 3) == 0):
                pdf.ln(10)
                pdf.cell(20)
            count +=1
    pdf.output(fpath , 'F')

writePDF()
