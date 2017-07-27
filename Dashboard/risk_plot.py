import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

tasks = pd.read_excel('tasks.xlsx')


final_df = pd.DataFrame()
clusters = ['GP1','GP2','PEC1','PEC2','SPLUNK','RESEARCH']


tasks.drop(['Task','Flag'],axis=1,inplace=True)

for cluster in clusters:
  
    
    # if cluster is not in list all green
    if cluster not in tasks['Cluster'].tolist():
        #np.max(tasks['ETA (days)'])
        green= pd.Series({'Cluster':cluster,
                          'Severity':'green',
                          'ETA (days)':tasks['ETA (days)'].max()})
      
        final_df = final_df.append(green,ignore_index=True)
        
    else:
    
        cluster_df = tasks[tasks['Cluster'] == cluster]

        ## account for ties
        max_entry = cluster_df.groupby('Cluster').agg(np.max).reset_index()
        max_color = max_entry['Severity']

        #print(max_entry)
        if (max_color == 'red').bool():
            # add red
            final_df = pd.concat([final_df,max_entry],ignore_index=True)

        elif (max_color == 'yellow').bool():
            # add red
            red = cluster_df[(cluster_df["Cluster"]==cluster) & (cluster_df["Severity"]=='red')]
            final_df = pd.concat([final_df,red],ignore_index=True)
            # add yellow
            final_df = pd.concat([final_df,max_entry],ignore_index=True)

        elif (max_color == 'blue').bool():
            # add red
            red = cluster_df[(cluster_df["Cluster"]==cluster) & (cluster_df["Severity"]=='red')]
            final_df = pd.concat([final_df,red],ignore_index=True)
            # add red
            red = cluster_df[(cluster_df["Cluster"]==cluster) & (cluster_df["Severity"]=='yellow')]
            final_df = pd.concat([final_df,red],ignore_index=True)
            # add blue
            final_df = pd.concat([final_df,max_entry],ignore_index=True)


## ADD green entries
no_green  = [x for x in clusters if x not in final_df[final_df['Severity']=='green']['Cluster'].tolist()]

for cluster in no_green:
    
    green= pd.Series({'Cluster':cluster,
                      'Severity':'green',
                      'ETA (days)':tasks['ETA (days)'].max()})

    final_df = final_df.append(green,ignore_index=True)
    
final_df.sort_values('Cluster',inplace=True)


## ADD all other entries with 0 ETA (blue, yellow, red)

no_blue  = [x for x in clusters if x not in final_df[final_df['Severity']=='blue']['Cluster'].tolist()] 
no_yellow  = [x for x in clusters if x not in final_df[final_df['Severity']=='yellow']['Cluster'].tolist()]
no_red  = [x for x in clusters if x not in final_df[final_df['Severity']=='red']['Cluster'].tolist()]

print('no red')
print(no_red)

for cluster in no_blue:  
    print(cluster)
    blue= pd.Series({'Cluster':cluster,
                      'Severity':'blue',
                      'ETA (days)':0})
    final_df = final_df.append(blue,ignore_index=True)
for cluster in no_yellow:    
    yellow= pd.Series({'Cluster':cluster,
                      'Severity':'yellow',
                      'ETA (days)':0})
    final_df = final_df.append(yellow,ignore_index=True)
for cluster in no_red:    
    red= pd.Series({'Cluster':cluster,
                      'Severity':'red',
                      'ETA (days)':0})
    final_df = final_df.append(red,ignore_index=True)
    
final_df.sort_values(['Cluster','Severity'],inplace=True)


fig, ax = plt.subplots(figsize=(7,5))

greens = final_df[final_df['Severity']=='green']
blues = final_df[final_df['Severity']=='blue']
yellows = final_df[final_df['Severity']=='yellow']
reds = final_df[final_df['Severity']=='red']


green = ax.barh(np.arange(len(clusters)),greens['ETA (days)'],color='g',align='center',height=0.4,edgecolor='black',alpha=0.8)
blue = ax.barh(np.arange(len(clusters)),blues['ETA (days)'],color='b',align='center',height=0.4,edgecolor='black',alpha=0.8)
yellow = ax.barh(np.arange(len(clusters)),yellows['ETA (days)'],color='y',align='center',height=0.4,edgecolor='black',alpha=0.8)
red = ax.barh(np.arange(len(clusters)),reds['ETA (days)'],color='r',align='center',height=0.4,edgecolor='black',alpha=0.8)


ax.set_yticklabels(['']  + clusters)
ax.set_xlabel('days')
ax.xaxis.grid(True)

#legend
red_patch = mpatches.Patch(color='red',
                           label='critical')
yellow_patch = mpatches.Patch(color='yellow',
                              label='moderate')
blue_patch = mpatches.Patch(color='blue',
                            label='slight')


ax.legend(handles=[red_patch,
                        yellow_patch,
                        blue_patch],bbox_to_anchor=(0.50, 1.1), loc='upper center', borderaxespad=0.,ncol=3,frameon=False)
 

ax.tick_params(bottom="off", top="off", left="off", right="off")
for key,spine in ax.spines.items():
        spine.set_visible(False)


fig.savefig('risk.png')
