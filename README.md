# AIMLSSE - API
The shortened term "AIMLSSE" stands for "AI/ML based Support for Satellite Exploration".

This API is designed to provide a basis for developing separate microservices that cooperate with the rest of the system by providing additional functionality. Among other things, this reduces coupling and increases cohesion, while contributing to better scalability.
For future work, the architecture should present a better overall maintainability and easier replacement of components in case of breakage.

## Structure
The interfaces defined by this API include:
- GroundDataAccess
    - Provides access to data of sensors on the earth
- SatelliteDataAccess
    - Provides access to data of satellites