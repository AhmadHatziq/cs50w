document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Process the user parameters when the user submitted the #compose-form form. 
  document.querySelector('#compose-form').onsubmit = () => {
    send_email();
    load_mailbox('inbox'); 
    
    // NTS: Set to false. If we set to true, will get broken pipe error. 
    // We will manually set the view to load_mailbox.  
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
      // Log result
      console.log(result.json());
      console.log(result);

      // Throw generic error if status code is not 201. 
      if (result.status != 201) {
        throw "Error in sending email"; 
      }; 

      // Throw Error if the term 'error' is in the returned JSON object. 
      if (JSON.stringify(result).includes('error')) {
        console.log(JSON.stringify(result)); 
        throw JSON.stringify(result);
      }

  })
  .catch(error => {
    console.log('Error:', JSON.stringify(error)); l
    alert('Error in sending message.\nPlease try again.', error); 
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
  // The function below changes the first letter to uppercase. 
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Query the API for the emails. 
  console.log(`Accessing for ${mailbox}`); 
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    // console.log(emails);

    // Create table and header row. 
    let email_table = document.createElement('table'); 
    let header_head = document.createElement('thead'); 
    let header_row = document.createElement("tr"); 
    let header_data_1 = document.createElement("th"); 
    let header_data_2 = document.createElement("th");
    let header_data_3 = document.createElement("th");
    header_data_1.textContent = "Sender"; 
    header_data_2.textContent = "Subject"; 
    header_data_3.textContent = "Timestamp"; 
    header_row.appendChild(header_data_1); 
    header_row.appendChild(header_data_2); 
    header_row.appendChild(header_data_3); 
    header_head.appendChild(header_row); 
    header_head.className = 'thead-dark'; 
    email_table.appendChild(header_head); 
    email_table.className = 'table'; 

    // Iterate over each email
    for (let i = 0; i < emails.length; i++) {

      // single_email represents a single JSON object. 
      // Extract relevant information from JSON object. 
      let single_email = emails[i];
      let is_read = single_email['read']; 
      let is_archived = single_email['archived']; 
      let sender = single_email['sender']; 
      let subject = single_email['subject']; 
      let body = single_email['body']; 
      let recipient_list = single_email['recipients']; 
      let timestamp = single_email['timestamp']; 
      let email_id = single_email['id']; 

      // Create table elements 
      let table_row = document.createElement("tr"); 
      let table_data_1 = document.createElement("td"); 
      let table_data_2 = document.createElement("td"); 
      let table_data_3 = document.createElement("td"); 

      // Set color to gray if email is read. 
      let color_string = 'white'; 
      if (is_read === true){ 
        color_string = 'lightgrey';
      }

      // Assign data to the row elements 
      table_data_1.textContent = sender; 
      table_data_2.textContent = subject; 
      table_data_3.textContent = timestamp; 

      // Make the email subject clickable when the user hovers (like an anchor) and send user to view that particular email. 
      table_data_2.addEventListener("mouseover", function() {
        table_data_2.style = 'color: blue; text-decoration: underline; cursor: pointer;'; 
      })
      table_data_2.addEventListener("mouseout", function() {
        table_data_2.style = ''; 
      })
      table_data_2.addEventListener("click", function() {
        show_single_email(email_id, mailbox); 
      }); 

      // Append row to the table 
      table_row.appendChild(table_data_1); 
      table_row.appendChild(table_data_2); 
      table_row.appendChild(table_data_3); 
      table_row.style.backgroundColor = color_string; 
      email_table.appendChild(table_row); 
      
      // Append table to document div. 
      let email_div_view = document.querySelector("#emails-view"); 
      email_div_view.appendChild(email_table); 
    }


    // ... do something else with emails ...
});

}

// Displays the contents of a single email. 
// Function is called when a subject title is clicked. 
function show_single_email(email_id, mailbox) {

  // Clear the emails-view of any content. 
  let email_div_view = document.querySelector("#emails-view"); 
  email_div_view.innerHTML = '';

  // Extract content of email and display to user. 
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    
    // Process email contents
    let is_read = email['read']; 
    let is_archived = email['archived']; 
    let sender = email['sender']; 
    let subject = email['subject']; 
    let body = email['body']; 
    let recipient_list = email['recipients']; 
    let timestamp = email['timestamp']; 
    let email_id = email['id']; 

    // Create div elements for email. 
    let single_email_div = document.createElement("div");
    single_email_div.innerHTML = `
      <h3> Email Details:</h3> <br>
      <h4> Subject: ${subject} </h4> <br>
      <h5> From: ${sender} </h5> 
      <h5> To: ${recipient_list} </h5> 
      <h6> Received timestamp: ${timestamp} </h6> <br>
      <h6> Email contents: </h6>
      <div class="card">
        <div class="card-body">
          ${body}
        </div>
      </div>
    `; 
    email_div_view.appendChild(single_email_div)

  });

}