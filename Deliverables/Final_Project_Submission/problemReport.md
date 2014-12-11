===
SEADS Front End Problem Report
---

| Bug Title        | How to Trigger Failure           | Location of Fault  | Possible Remedy |
| ------------- |:-------------:| -----:|-----:|
| Visualize other peoples plugs      | Manually navigate to visualization/<deviceID> | Visualization | Add check for request.currentuser.id vs passed in id variable |
| Invalid Data Reaction Needs Improvement: Causes Lock on Graph      | Select a date out of the range where there exists valid data.       |   Visualization | Add a check: If the user chooses a date out of range, show a message on the graph.|
| Attempting to access the visualization view while not logged in is possible if a correct device ID is passed into the URL | Manually enter root directory address + /visualization/<deviceID>      |    Visualization | Add user authentication python decoration to visualization definition.|
