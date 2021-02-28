# Epidemic
Simulation study on epidemic  based on Network Science. 
COVID-19 as a new type of virus was announced as epidemics and had made huge impact on human society. Those different simulation models
are built to study about the spread of COVID-19.

First of all, there are some assumptions for the simulation models which assumptions are based on the characteristics and status of COVID-19. 
The assumptions of virus as follow:
1. All the healthy people can be infected by their infected neighbours with a probability that follows the logarithmic distribution.
2. All the infected people can recovery with a certain probability that follows the normal distribution.
3. All the infected people will died with a probability that follows an inverse function.
4. For the scenario that consider the asymptomatic virus carriers, the rate that the patient show some symptom is linear increase.

(specific content is mention in epidemic.py, the distributions is shown as follow)
![Image text](https://github.com/arialibra/Epidemic/blob/master/IMG-folder/assumptions.jpg)
![Image text](https://github.com/arialibra/Epidemic/blob/master/IMG-folder/infenction.jpg)

In addition, it is assumed that there are total 300 individuals in the environment to compare the results from diverse situations. In the model, 10% people are randomly selected and be decided as the patients who have symptom. Meanwhile, there are another 10% people who actually get infected but have no symptoms.


Part I - Study on Isolation Method
Model 1:
Completely isolation - everyone is immediately isolated from each other if there are infected people exist in the environment.
Finally, The average final number of rest healthy people, recovery people, dead people are respectively 230, 63 and 7. No patients at all need average 14 days. This is the fastest way to get society back to normal.
![Image text](https://github.com/arialibra/Epidemic/blob/master/IMG-folder/model1.jpg)

Model 2:
Partial isolation - the person is isolated from the outside world after he or she has sick.
Finally, The average final number of rest healthy people, recovery people, dead people are respectively 3, 267 and 30. No patients at all need average 20 days. Because of the hidden attribution for this virus, nearly 100% people in the network are infected which means this isolation approach has no effect.
![Image text](https://github.com/arialibra/Epidemic/blob/master/IMG-folder/model2.jpg)

Model 3:
Timely isolation - considers the history of the records of people contacted, if anyone has symptoms, the touch persons in his or her touch history might be infected, so he or she and those people in the list will be isolated.
Finally, The average final number of rest healthy people, recovery people, dead people are respectively 168, 122 and 10. No patients at
all need average 18 days. This isolation method by recording touch history is effective and efficient. Most importantly, few people who are not suspected to infected and recovery humans can continue to work during the isolation period.
![Image text](https://github.com/arialibra/Epidemic/blob/master/IMG-folder/model3.jpg)


Part II - Study on Hospital Stategy
The isolation strategies mentioned before do not involve any medical resources. Start from this model, hospital begins to be considered in models. Obviously, the current medical resources cannot meet the needs of patients, so not all the patients can be accepted by the hospital. In models, I assumed hospital can accommodate 5% of the total humans which means the volume of the hospitals is v = 15. Moreover, We only isolate the patients who are in hospital with each other rather than the patients who are not in the hospital in the network in order to better compare the recovery consequences of those two models.

Model 4:
Hospital admission in sequential - the patients that accepted by the hospital are decided by the order of the people get infected. In another word, people who are infected first can go to the hospital earlier than the people get infected later, no matter whether their states are severe or mild.
Finally, no patients at all need average 36 days and the average final number of recovery people and dead people are respectively 260 and 40.
![Image text](https://github.com/arialibra/Epidemic/blob/master/IMG-folder/model4.jpg)

Model 5:
Hospital admission in severity - hospital rule is that the earlier the infection time, the higher the priority is employed to decide the order of accessing in hospital and this order is updated each day. All the people infected at current time will be evaluated.
Finally, The condition that no patients in the environment needs average 36 days and the average final number of recovery people and dead people are 280 and 20 respectively. Therefore, good strategy to decide the sequence of hospital acceptance such as based on the possible infection time can speed up the recovery of the society under the condition that the medical resources are limited.
![Image text](https://github.com/arialibra/Epidemic/blob/master/IMG-folder/model5.jpg)

To sum up, I think isolation is necessary to stop spreading the virus and timely isolation is useful. Recording the contact history can help to control the spread of the virus. In addition, hospital accept the patient according to the severity has better performance. Thus, Combining these two approaches, timely isolation and hospital admission severity, maybe better stop the virus from getting worse and get back to normal faster.
