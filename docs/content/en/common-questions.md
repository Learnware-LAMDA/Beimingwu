# Common Questions

### Q1: How does the Beimingwu system protect user data privacy?

A1: In the Beimingwu system, the uploading, searching, and deployment of learnwares do not require users to upload local data. The statistical specifications are generated locally by the user using open-source API and do not compromise the raw data's security.


### Q2: How does the Beimingwu system ensure the safety of deploying learnware?

A2: We make every effort to verify the safety of each learnware and provide interfaces for deploying learnware within a docker container.


### Q3: What types of data does the Beimingwu system support for learnware?

A3: We support various data types, including tables, images, and texts.


### Q4: How to initiate heterogeneous table search?

A4: When the regular search returns an empty list, the system will suggest heterogeneous search. You will need to provide additional semantic information for each feature, which can be manually entered or uploaded by a JSON file containing feature semantic information, then proceed the search.


### Q5: Why doesn't the learnware show up in the system after submission?

A5: After learnware is submitted, the system automatically adds it to a validation queue. The  results will be displayed in the web section "Personal Information - My Learnware", and only those that pass the validation will be displayed in the system. It is recommended to validate the learnware locally using the `learnware` package before submission.
