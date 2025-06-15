# Logs Framework Manual:

# 1. Overview:
This document describes the internal tutorial recommendation system.
Its purpose is to provide personalized suggestions of upcoming tutorials to students based on their previous preferences and tutorial attributes using a weighted scoring algorithm. This improves user experience and educational effectiveness.

# 2. Importing the Framework:

To include the log framework in a determined module or script, import the 
following packages included in the repository files:

```python
from app.services.recommendation import get_tutoring_recommender
```


# 3. Recommendation Logic:
The strategy assigns a score to each available tutorial that the student has not yet registered for, adding points based on:

- Subject similarity to previously taken tutorials

- Matching method (virtual or presencial) with the most common method among tutorials previously taken.

- If the tutorial is taught by a preferred tutor (one who has taught the student before).

- A penalty based on remaining capacity, favoring tutorials with fewer seats left to encourage early enrollment.

**Parameters:**
1) repository: The firestore repository containing the tutorials and user data.
2) student_id: The unique identifier of the student for whom recommendations are being generated.


### Example Usage:
```python
from app.services.recommendation import get_tutoring_recommender
repository = ...  # Initialize your repository here
student_id = "student123"
recommender = get_tutoring_recommender(repository, student_id)
```
