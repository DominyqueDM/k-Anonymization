# k-Anonymization

This was my dissertation project. The basis of the idea was to create create an educational tool that would allow lecturers to teach and better showcase the importance of anonymisation algorithms. The anonymisation algorithm chosen here is the K Anonymisation Using Clustering Technique. 

What will the algorithm show? 
 - It evaluated its efficiency in terms of data utility/ information loss and running time,
 - Created a user interface for users to easily run the algorithm with a pre-loaded dataset and receive metrics.
 - Providing the user with a breakdown of how the algorithm works, as well as an anonymised version of their dataset. 
 
 A key part of this k-anonymisation approach is the clustering technique that has been added. Clustering, as we know it, is the process of grouping similar objects together, and this concept carries on for this approach but is altered slightly. In terms of k-anonymisation using clustering, it is the process of grouping similar records together but each cluster/group needs to contain at least k records. Therefore, if k is set to 5, each cluster will need to have at least 5 similar records- no less. Fig 2 shows one way how 15 data points/records would be clustered. There is no limit on how many clusters you can or cannot have, the only requirement is the minimum number of records in the cluster. 
How do we determine which records are similar? The closest data points are connected to form a cluster and then the next closest data point to those initial data points is then added to form a bigger cluster. This approach iteratively does this until each cluster has at least the minimum number of records allowed, which is k. 

Below shows the data flow of the project: 
![image](https://user-images.githubusercontent.com/43965970/214062571-e6aee3b4-9382-4f97-8b76-b3742e333108.png)

 Below shows the interface screens: 
 ![image](https://user-images.githubusercontent.com/43965970/214062885-5ac83263-ec06-4431-8956-1e795fe85188.png)

 ![image](https://user-images.githubusercontent.com/43965970/214062921-ee6845dd-e48f-450c-a6ac-dfa6a2cbeb93.png)

![image](https://user-images.githubusercontent.com/43965970/214062955-cab04aa3-77ec-4c16-805b-b26524994d8f.png)

![image](https://user-images.githubusercontent.com/43965970/214062986-b800ac6f-7944-4879-a881-cf537d23b7aa.png)

![image](https://user-images.githubusercontent.com/43965970/214063017-2af1711b-3225-4c7f-8af7-8f8d5f30792d.png)

![image](https://user-images.githubusercontent.com/43965970/214063044-06bdf163-8ffd-4123-b6a7-2ff7273cf404.png)
