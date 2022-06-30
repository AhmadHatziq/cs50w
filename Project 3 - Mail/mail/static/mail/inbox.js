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

function send_email() {
  alert('Send email');
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