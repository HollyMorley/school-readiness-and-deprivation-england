# Plan

1. Predict early years foundation stage score (EYFSP) from A) index of multiple deprivation (IMD) and B) individual
   indices of deprivation (IOD: income, employment, education, health, crime, barriers to housing and services, living
   environment).
2. Compare prediction model across multiple years.
3. Find important features of the IODs for predicting EYFSP (e.g. leave-one-out).
4. Find residuals for each LA and try to predict these using other scores (TBC but e.g. teacher quality, school funding,
   extracurricular activities, alumni visits? N.B. probably need to regress out the IODs or IMD first to get the
   residuals, otherwise the IODs will likely be the most important features in this model)
5. Separately, predict a later educational outcome (e.g. GCSEs) from the same deprivation scores and see if the same
   patterns hold
6. (Try to predict EYFSP from the IODs using e.g. neural networks - mostly for personal practice)