const express = require('express');
const bodyParser = require('body-parser');

const dialogflow = require('@google-cloud/dialogflow');
const uuid = require('uuid');

config = {
    keyFilename: "./plp-smartbookguide-skb9-2d437663ab38.json"
}
const sessionClient = new dialogflow.SessionsClient(config);
console.log(sessionClient);
const sessionId = uuid.v4();
const sessionPath = sessionClient.projectAgentSessionPath("plp-smartbookguide-skb9", sessionId);

/**
 * Send a query to the dialogflow agent, and return the query result.
 * @param {string} projectId The project to be used
 */
async function callDialogflow(user_text) {
    console.log(user_text);
  // A unique identifier for the given session
  // The text query request.
  const request = {
    session: sessionPath,
    queryInput: {
      text: {
        // The query to send to the dialogflow agent
        text: user_text,
        // The language used by the client (en-US)
        languageCode: 'en-US',
      },
    },
  };

  // Send request and log result
  const responses = await sessionClient.detectIntent(request);
  console.log('Detected response');
  console.log(responses);
  const result = responses[0].queryResult;
  console.log(`  Query: ${result.queryText}`);
  console.log(`  Response: ${result.fulfillmentText}`);
  if (result.intent) {
    console.log(`  Intent: ${result.intent.displayName}`);
    return result.fulfillmentText
  } else {
    console.log(`  No intent matched.`);
    return "bad result :("
  }
    
}

const app = express();
const port = process.env.PORT || 5000;

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.get('/api/hello', (req, res) => {
  res.send({ express: 'Hello From Express' });
});

app.post('/api/world', (req, res) => {
  console.log(req.body);
  callDialogflow(req.body['user_input'])
    .then((fulfilmentText)=>{
        console.log(`${req.body['user_input']}, ${fulfilmentText}`);
        res.send(
            {response:`${fulfilmentText}`},
        );
    })

});

app.listen(port, () => console.log(`Listening on port ${port}`));