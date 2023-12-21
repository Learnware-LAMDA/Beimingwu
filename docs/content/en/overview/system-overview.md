# Beimingwu: A Learnware Dock System

Beimingwu is based on the Learnware paradigm, which systematically implements the entire process of learnware from submission to deployment, helping users effectively search and reuse learnwares without the need to build machine learning models from scratch.

## What is Learnware?

A learnware consists of high-performance machine learning models and specifications that characterize the models, i.e., "Learnware = Model + Specification."

The learnware specification consists of "semantic specification" and "statistical specification":
- semantic specification describes the type and functionality of the model through text.
- statistical specification characterizes the statistical information contained in the model using various machine learning techniques.

Learnware specifications describe the model's capabilities, enabling the model to be identified and reused by future users who may know nothing about the learnware dock system in advance.

## Why Do We Need the Learnware Dock System?

Machine learning has achieved great success in many fields but still faces various challenges, such as the need for extensive training data and advanced training techniques, the difficulty of continuous learning, the risk of catastrophic forgetting, and the leakage of data privacy.

Although there are many efforts focusing on one of these issues separately, they are entangled, and solving one problem may exacerbate others.

The learnware dock system aims to address many of these challenges through a unified framework:
- **Lack of Training Data/Skills**: Even for ordinary users with limited data and machine learning knowledge, they can obtain powerful machine learning models from the learnware dock system. Users can acquire high-performance learnwares and further customize or improve them without starting from scratch.
- **Continuous Learning**: As high-performance learnware is continually submitted for various tasks, the knowledge in the learnware dock system will naturally accumulate, achieving continuous and lifelong learning.
- **Catastrophic Forgetting**: Once learnware is accepted, it will always be retained in the learnware dock system unless it can be replaced by other learnware in all aspects. Therefore, old knowledge in the learnware dock system is always preserved and never forgotten.
- **Data Privacy/Ownership**: Developers only submit models without sharing private data, thus protecting data privacy and ownership. Although the possibility of reverse engineering the model cannot be completely eliminated, the risk of privacy leakage in the learnware dock system is minimal compared to many other privacy protection schemes.

## How Does the Learnware Dock System Work?

The learnware dock system is the core entity in the Learnware paradigm. In the learnware paradigm, there are three essential entities:
- **Developers**: Typically machine learning experts who produce and wish to share/sell their high-performance machine learning models.
- **Users**: In need of machine learning services but often have limited data and lack machine learning knowledge and skills.
- **Learnware Dock System**: Receives high-performance machine learning models from developers, incorporates them into the system, and provides services to users by identifying and reusing learnware to help users solve current tasks.

As shown in the diagram below, the system workflow consists of two stages:

- **Submitting Stage**: Developers voluntarily submit various learnwares to the learnware dock system, and the system conducts quality checks and further organization of these learnwares.
- **Deploying Stage**: When users submit task requirements, the learnware dock system automatically selects whether to recommend a single learnware or a combination of multiple learnwares and provides efficient deployment methods. Whether it's a single learnware or a combination of multiple learnwares, the system offers convenient learnware reuse interfaces.

![image](.../../../../public/overview/learnware_workflow.svg)

### Specification World

Specification is the core component of the learnware dock system, linking all processes about learnwares, including uploading, organizing, searching, deploying, and reusing.

Learnwares from different feature/label spaces form numerous islands of specifications, and all these islands together constitute the "specification world" in the learnware dock system. In the specification world, if connections between different islands can be discovered and established, the corresponding islands of specification can be merged.

![image](../../public/overview/specification_world.jpg)

When searching in the learnware dock system, the system first identifies specific islands of specifications based on semantic specifications in user requirements, and then it accurately recognizes learnwares on the specification islands through statistical specifications in user requirements.

Merging different specification islands means that the corresponding learnwares can be used in tasks with different feature/label spaces, i.e., they can be reused in tasks beyond their original purposes.

## What Features Does the Beimingwu System Have?

Beimingwu systematically implements the core process of the learnware paradigm for the first time:

- **Submitting Stage**: The system includes multiple detection mechanisms to ensure the quality of uploaded learnwares. Additionally, the system trains a heterogeneous engine based on existing learnware specifications in the system to merge different specification islands and assign new specifications to learnwares. With more learnwares are submitted, the heterogeneous engine will continue to update, achieving continuous iteration of learnware specifications and building a more precise specification world.
- **Deploying Stage**: After users upload task requirements, the system automatically selects whether to recommend a single learnware or multiple learnware combinations and provides efficient deployment methods. Whether it's a single learnware or a combination of multiple learnwares, the system offers convenient learnware reuse tools.

In addition, the Beimingwu system also has the following features:

- **Learnware Specification Generation**: The Beimingwu system provides specification generation interfaces in the `learnware` Python package, supporting various data types (tables, images, and text) for efficient local generation.
- **Learnware Quality Inspection**: The Beimingwu system includes multiple detection mechanisms to ensure the quality of each learnware in the system.
- **Diverse Learnware Search**: The Beimingwu system supports both semantic specifications and statistical specifications searches, covering data types such as tables, images, and text. In addition, for table-based tasks, the system also supports the search for heterogeneous table learnwares.
- **Local Learnware Deployment**: The Beimingwu system provides interfaces for learnware deployment and learnware reuse in the `learnware` Python package, facilitating users' convenient and secure learnware deployment.
- **Data Privacy Protection**: The Beimingwu system operations, including learnware upload, search, and deployment, do not require users to upload local data. All relevant statistical specifications are generated locally by users, ensuring data privacy.
- **Fully Open Source**: The Beimingwu system's source code is completely open-source, including the `learnware` Python package and frontend/backend code. The `learnware` package is highly extensible, making it easy to integrate new specification designs, learnware system designs, and learnware reuse methods in the future.

Beimingwu is the first system-level implementation of the learnware paradigm, and there is still much room for improvement in related technologies. We invite you to experience it and provide valuable feedback for the continuous improvement of the system.