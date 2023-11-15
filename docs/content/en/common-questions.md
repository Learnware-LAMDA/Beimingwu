# Common Questions

### Q1: How does the Beimingwu system protect user data privacy?

A1: In the Beimingwu system, the submission, searching, and deployment of learnware do not require users to upload local data. All involved statistic specifications are generated locally by the user and do not expose original data, ensuring your data privacy.


### Q2: How does the Beimingwu system ensure the safety of deploying learnware?

A2: We make efforts to verify the safety of each learnware and provide tools for deploying learnware within a `docker` container.


### Q3: What types of data does the Beimingwu system support for learnware?

A3: We support various data types, including tables, images, and texts.


### Q4: How to initiate heterogeneous table search?

A4: When regular searches return an empty list, the system will suggest heterogeneous search. You will need to provide additional semantic information for each dimension feature, which can be manually entered or uploaded as a `json` file containing feature semantic information, then proceed with the search.


### Q5: Why doesn't the learnware show up in the system after submission?

A5: After learnware is submitted, the system automatically adds it to a validation queue. The  results will be displayed in the web section "Personal Information - My Learnware", and only those that pass the validation will be displayed in the system. It is recommended to validate the learnware locally using the `learnware` package before submission.
