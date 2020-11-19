
# https://daviddalpiaz.github.io/r4sl/elastic-net.html
# http://faculty.marshall.usc.edu/gareth-james/ISL/


# --------------------------------------------------------------------------------------------------------- #
# -- project: Plateau, a Calibration Technique for Trading Systems Optimization                          -- #
# -- File: rmodel.r | Model fit with R                                                                   -- #
# -- author: IFFranciscoME                                                                               -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/IFFranciscoME/A1_Plateau_Calibration                                 -- #
# -- --------------------------------------------------------------------------------------------------- -- #

# Remove objects from enviornment
rm(list=ls())

# load libraries
library(olsrr)    # OLS statistical tools
library(rsample)  # data splitting
library(glmnet)   # implementing regularized regression approaches
library(dplyr)    # basic data manipulation procedures

# Set working directory to source file location
setwd("~/github/MSC/IDI-III/A1_Plateau_Calibration/")

source(paste0(getwd(), '/codes/visualizations/visualization.r'))

# -- ------------------------------------------------------------------------ Leer y preparar los datos -- #

fr_read_data <- function(r_file) {
    #' @title fr_read_data - Documentation
    #' 
    #' @description Function to read and clean a dataframe provided from 
    #' reading a csv file with the candidate features
    #' 
    #' @param r_file char. filename with the data generated by feature engineering process
    #' 
    #' @return Returns the same dataframe with all character columns as character and parameter 
    #' columns as numeric
    
    # data file
    file <- paste0("codes/data/features/", r_file)
    
    # Load data
    data <- read.csv(file, header = TRUE)
    
    # do not include timestamp and co_d columns in dataframe
    data_m <- data[, !names(data) %in% c("timestamp", "co_d")] 
    
    return (data_m)
}

# despues de leer features
data_f <- fr_read_data(r_file='data_features.csv')

# tabla de nombres de variables y etiquetas
nombres <- as.character(colnames(data_f))
t_coeficientes <- data.frame(coef=c(nombres),
                             var=c('y', paste0('x_', seq(1, length(colnames(data_f))-1, 1))),
                             stringsAsFactors = FALSE)
# colnames(data_f) <-  t_coeficientes$var

# -- ----------------------------------------------------------------------------- Analisis de variables -- #

# matriz de correlaciones
correlaciones <- cor(data_f)

# datos para grafica de correlacion con variable dependiente
datos <- data.frame(features=colnames(data_f)[2:length(data_f)],
                    correlaciones=cor(data_f)[2:length(data_f), 1],
                    signo=ifelse(data_f[2:length(data_f), 1] < 0, -1, 1))

# plot de correlacion entre variables independientes y variable dependiente
triggers <- c(-0.25, 0.25)
vs_corr <- vr_corrplot(r_datos=datos, r_triggers=triggers)
vs_corr

# mapa de calor de correlaciones entre variables independientes
vs_mcorr <- ggCorHM(Data = correlaciones, Nombres = colnames(correlaciones), OrdType =  "Ordenado",
                    ColorLow = "sky blue", ColorHigh = "steel blue", ColorMid = "white", TamTxtCor = 2,
                    RndTxtCor = 1, ColTxtCor = "black")
vs_mcorr


# -- ---------------------------------------------------------------------- Mejor modelo sin regularizar -- #

# ajuste de modelo "General"
modelo_1 <- lm(co ~ . -1, data = data_f[,1:30], na.action = na.fail)

# Responde con NA en algunas variables por que estas estan linealmente relacionadas con otras variables,
# y cuando esto sucede no hay una solucion unica a la regresion sin que tenga que quitarse alguna de las
# variables.

# coeficientes ajustados
modelo_1$coefficients

# quitando los coeficientes con NA
formula <- as.formula(paste0("y ~ ", round(na.omit(coefficients(modelo_1)[1], 2)), "", 
                             paste(sprintf(" %+.2f*%s ", na.omit(coefficients(modelo_1))[-1],  
                                           names(na.omit(coefficients(modelo_1)[-1]))), collapse="")))
formula

# Diagnostico de colinelidad entre variables explicativas
ols_vif_tol(modelo_1)

# Importancia relativa de cada variable en el modelo
ols_correlations(modelo_1)

# Plots de diagnostico
ols_plot_diagnostics(modelo_1)

# Stepwise Forward Regression
mejor_pasos <- ols_step_forward_p(modelo_1)

# -- plots de resultados
plot(mejor_pasos)

# -- Variance inflation factors
ols_vif_tol(mejor_pasos$model)

# Importancia relativa de cada variable en el modelo
ols_correlations(modelo_1)

# -- modelo 
modelo_2 <- mejor_pasos$model

# -- plot de residuales
modelo_3 <- ols_step_forward_aic(modelo_1)
plot(modelo_3$model)

# -- ------------------------------------------------------------------- Mejor modelo con regularizacion -- #


# Diferencias en parametros segun observacion influencia
# ols_plot_dfbetas(model)

# correlacion entre variables independientes y variable dependiente MARCA ERROR
# ols_correlations(model)

# Todas las posibles regresiones
# k <- ols_step_all_possible(model)
# plot(k)
