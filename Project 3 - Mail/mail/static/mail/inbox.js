document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Process the user parameters when the user submitted the #compose-form form. 
  document.querySelector('#compose-form').onsubmit = () => {
    send_email();
    load_mailbox('sent'); 
    
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

  

};

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
};

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

      // Set color to gray if email is read. Color is white if not read. 
      let color_string = 'white'; 
      if (is_read){ 
        color_string = 'lightgrey';
      } else {
        color_string = 'white'; 
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

};

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

    // Mark this email as read. 
    is_read = true; 
    fetch(`/emails/${email_id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read:true
      })
    })

    // Create div elements for email contents. 
    // Include buttons for replying, marking as read and archiving/unarchiving
    // Read and Archiving buttons will change depending on current email state. 
    let single_email_div = document.createElement("div");
    let read_button_string = 'Mark as Read'; 
    if (is_read) {
      read_button_string = 'Mark as Unread'; 
    }
    let archive_button_string = 'Archive';
    if (is_archived) {
      archive_button_string = 'Unarchive'; 
    }
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
      <br>

 
    `;

    // Create reply button 
    let reply_button = document.createElement("button");
    reply_button.className = 'btn btn-primary'; 
    reply_button.innerText = 'Reply'; 
    reply_button.id = 'reply_button'; 
    reply_button.addEventListener('click', () => load_reply_email(sender, subject, body, timestamp));
    single_email_div.appendChild(reply_button); 
    single_email_div.appendChild(document.createElement("br")); 
    single_email_div.appendChild(document.createElement("br")); 

    // Create mark-as-read/unread button. 
    let read_button = document.createElement('button'); 
    read_button.className = 'btn btn-success'
    read_button.innerText = `${read_button_string}`; 
    read_button.id = 'read_button'; 
    read_button.addEventListener('click', () => mark_email_as_read(email_id)); 
    single_email_div.appendChild(read_button); 
    single_email_div.appendChild(document.createElement("br")); 
    single_email_div.appendChild(document.createElement("br")); 

    // Create archive/unarchive button for mails not in sentbox 
    if (!mailbox.includes('sent')) { 
      let archive_button = document.createElement('button'); 
      archive_button.className = 'btn btn-warning';
      archive_button.innerText = `${archive_button_string}`;  
      archive_button.id = 'archive_button'; 
      archive_button.addEventListener('click', () => mark_email_as_archive(email_id)); 
      single_email_div.appendChild(archive_button); 
      single_email_div.appendChild(document.createElement("br")); 
      single_email_div.appendChild(document.createElement("br")); 
    }; 


    // Append email div back to original email view div. 
    email_div_view.appendChild(single_email_div)

  });

};

// Handles marking an email as archived or unarchived. 
// email_id is the int representing email ID. 
function mark_email_as_archive(email_id) {

  // Fetch the email to get the current archive status. 
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {

    let current_archive_status = email['archived']; 

    if (current_archive_status) {

      // Send API call to set status as unarchived. 
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: false 
        })
      }); 

      // Update button text to reflect the change to the user. 
      let button_text = 'Archive'; 
      let archive_button = document.getElementById('archive_button');
      archive_button.innerText = button_text; 

    } else {

      // Send API call to set status as unarchived. 
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: true 
        })
      }); 

      // Update button text to reflect the change to the user. 
      let button_text = 'Unarchive'; 
      let archive_button = document.getElementById('archive_button');
      archive_button.innerText = button_text; 
    }

  });

  // Once an email has been archived or unarchived, load the user's inbox. 
  load_mailbox('inbox');

};

// Handles marking an email as read or unread.
// email_id is the int representing email ID. 
function mark_email_as_read(email_id) {

  // Made function retrieve email again to keep it modular. 
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    let current_read_status = email['read']; 

    if (current_read_status) {

      // Send API call to set status as unread 
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read:false 
        })
      }); 

      // Change button text to display the change to the user 
      let button_text = 'Mark as Read'
      let read_button = document.getElementById('read_button');
      read_button.innerText = button_text; 

      //console.log(`Marked as unread for ${email_id}`);

    } else {

      // Send API call to set status as read
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read:true
        })
      }); 

      // Change button text to display the change to the user 
      let button_text = 'Mark as Unread'
      let read_button = document.getElementById('read_button');
      read_button.innerText = button_text; 

      //console.log(`Marked as read for ${email_id}`);
    }; 

  }); 
}; 

// Loads up email composition form with 3 fields pre-filled: recipient, subject, body. 
function load_reply_email(sender, subject, body, timestamp) {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
  
    // Pre-fill up composition fields
    document.querySelector('#compose-recipients').value = `${sender}`;
    document.querySelector('#compose-subject').value = `Re: ${subject}`;
    document.querySelector('#compose-body').value = `On ${timestamp} ${sender} wrote: ${body} \n\n`;

};