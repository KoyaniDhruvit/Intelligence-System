The JSON object contains two arrays:
	- The resources array contains all resources with their respective IDs
	- the jobs array contains all jobs. Each job has an ID and an operations array containing its operations
		- The operations contain their index in the order of operations, their duration, and the resource the operation must be executed on.

minimal example:

{
  "resources": [
    {
      "id": 0
    }
  ],
  "jobs": [
    {
      "id": 0,
      "operations": [
        {
          "index": 0,
          "duration": 1,
          "resource": 0
        }
      ]
    }
  ]
}