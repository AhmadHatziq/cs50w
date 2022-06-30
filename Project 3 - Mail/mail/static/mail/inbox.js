document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Process the user parameters when the user submitted the #compose-form form. 
  document.querySelector('#compose-form').onsubmit = () => {
    send_email();
    
    // Return false temporarility for debugging. Will change to true once fully implemented. 
    return false;
  };

  // NTS: There are 2 ways to attach an event to the form, either addEventListener or altering the onsubmit.  
  /*
  document.querySelector('#compose-form').addEventListener('submit', function() {
    console.log("Email compose form has been submitted. "); 
    
    return false; 
  });
  */ 


  // By default, load the inbox
  load_mailbox('inbox');
});

// Function to process the sending of emails. 
// Is called when the compose-form is submitted. 
function send_email() {
  console.log('Sending email'); 

  // Extract parameters from the user
  const email_recipient = document.querySelector('#compose-recipients').value; 
  const email_subject = document.querySelector('#compose-subject').value; 
  const email_body = document.querySelector('#compose-body').value; 

  // Log to console. 
  let composed_email_log = `Email is for '${email_recipient}' with subject '${email_subject}' with body '${email_body}'`;
  console.log(composed_email_log);

  // Send email to API 
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: email_recipient,
        subject: email_subject,
        body: email_body
    })
  })
  .then(response => {
    console.log(response); 
    return response
  })
  .then(result => {
      // Print result
      console.log(result.json());

      // Throw generic error if status code is not 201. 
      if (result.status != 201) {
        throw "Error in sending email"; 
      }; 

      // Throw Error if the term 'error' is in the returned JSON object. 
      if (JSON.stringify(result).includes('error')) {
        throw JSON.stringify(result);
      }

  })
  .catch(error => {
    console.log('Error:', error); 
    alert('Error in sending message\n', error); 
  });

  return;

};

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}