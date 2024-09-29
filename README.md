# Robot Vacuum
This repo contians that code for a "robot vacum", the project contains a http-server plus a postgres database for storage.



# How to use
To run this project you need docker compose, simply run:
```
docker compose up
```

To access the api-spec go to:
```
http://localhost:5050/docs
```

# Details
FastApi is used for the http-server-framework and postgres for the storage.

The core logic can be found in `/src/robot`. To get a quick overview on the code you can look at the tests cases in the `/tests` folder.


# Approach
My intial thought was to keep track of each visited coordinate seperately, this approach is according to me most align with my understanding on how a robot-vacuum works.

However, looking at the specs in the case I saw it was not really feasible. With some not so correct estimation we could in theory visit a bit under `100 000 000` cordinates (10 000 * 100 000). This is a bit to much so save as (x, y)-pair.

Instead I decided to take a algorithmic approach, where I save horizontal and vertical movement in "intervals", leveraging the fact that the robot moves in straight lines. When counting unique visited coordinates the logic is to first count vertical and horizontal movements separately, and then deduct the overlap.




# Testing
Getting the right amount of tests are hard, but I am happy with the outcome of my tests here, while its not perfect it does a good job getting high coverage with little overlap and few tests.

I tried to test functionallity over implementation, and tried to write the test so they act as documentation of the code.


`test_api.py` - Mainly to test that the http-part is working as intended, we do not test any logic here, mostly the behaviour of the server.

`test_database.py` - Mainly to make sure our db-session actually in performing commits/rollbacks when needed.

`test_robot.py` - This file tests the core logic, making sure that the application is behaving as expected from a "business logic"-perspective.


`test_memory.py` - This file do have overlap with the tests in `test_robot.py`, in the end we test the logic in `memory.py` in the `test_robot.py`. However, the logic in `memory.py` is relative complex. While I am not a TDD-person I took a TDD-approach for developing `memory.py`. Started with the test and then implemented the logic. For "algorithmic"-logic with clear input/output this is a great workflow.


To run test you need poetry, then run:
```
poetry install
```

```
poetry run pytest ./tests
```



### Notes

`.env` - I removed the entry in `.gitignore` since it does not contain any real secrets and makes the process of running more smoother. 