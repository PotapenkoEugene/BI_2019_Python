# Задание 1
data <- mtcars
result <- shapiro.test(data$hp)
0.5  > result$p.value # нулевая гипотеза подтверждается => распределение нормальное
result_cyl <-by(data$hp, INDICES = data$cyl, shapiro.test) 
# 4 cyl  p-value = 0.2187  не норм распределение
# 6 cyl p-value =  0.002939 норм распределение
# 8 cyl p-value = 0.1047 не норм распредление
# пришел к такому выводу т.к. Ho шапиро-уилко теста = распределение нормальное

# Задание 2
am_hp_median <-data[data$am == 0 & data$hp > median(data$hp),] 
length(am_hp_median) # 11 машин с автоматом и hp больше медианного значения
result <- sort(am_hp_median, decreasing = TRUE) # чет я забыл как сортировать датафрейм по колонке =\\

