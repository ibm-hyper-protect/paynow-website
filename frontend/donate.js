/*##############################################################################
# Copyright 2019 IBM Corp. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
##############################################################################*/
// Backend database to GET and POST donations to
const BACKEND = "http://localhost:5000/api/v1/transactions";

// Used to select random people photos
function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1) + min);
}

// Get current donations on page load
$(document).ready(getDonations());

// When the website user clicks the donate button, send their details
// to the backend and update the page
$("#donateButton").click(function () {

  var donateJSON = {
    fundraising_event: "Isabel_Hurricane_Relief",
    name: $('#formName').val(),
    email: $('#formEmail').val(),
    location: $('#formCountry').val(),
    contribution: $('#donationAmount').val()
  };

  console.log("Sending : " + JSON.stringify(donateJSON));

  $.ajax({
    type: "POST",
    url: BACKEND + "",
    contentType: "application/json; charset=utf-8",
    data: JSON.stringify(donateJSON),
    success: function (msg) {
      console.log("MongoDB Id " + JSON.stringify(msg));

      // Change the button text
      $("#donateButton").prop('value', 'Thank you!');

      // Clear the fields
      $('#formName').prop('value', '');
      $('#formEmail').prop('value', '');
      $('#ccNum').prop('value', '');
      $('#ccCVV').prop('value', '');
      $('#donationAmount').prop('value', '$');

      // Scroll down to show the donation results
      setTimeout(function () {
        document.querySelector('#donate-results').scrollIntoView({
          behavior: 'smooth'
        });

        // Get the current donations again (repopulate the HTML)
        getDonations();

        // Change the donation button back
        $("#donateButton").prop('value', 'Donate');
      }, 1000);
    },
    error: function (XMLHttpRequest, textStatus, errorThrown) {
      console.log("Error : " + textStatus + "Error Thrown : " + errorThrown);
    }
  });
});



// Fetch the donations from the backend database and insert it into
// the donations page.
function getDonations() {
  $.ajax({
    type: "GET",
    url: BACKEND + "",
    dataType: "json",
    success: function (msg) {
      console.log("Success : " + JSON.stringify(msg));

      // No new donations, try again in a few seconds
      if (msg.length == 0) {
        console.log("Backend DB empty");
        $("#donate-results").html(`<p class="zero">Zero donations: be the first!</p>`);
        return;
      }

      var donatorList = msg.reverse();
      console.log("Success. Retrieved " + msg.length + " records from backend");

      // Chopping it up so we only show latest 5 contributions
      // console.log(donatorList.slice(0, (donatorList.length < 5 ? donatorList.length : 5)));
      var donator = "";
      $.each(donatorList, function (index, value) {

        donator = donator + `<div class="donation">
                    <p class="name">` + value.name + `</p>
                    <img src="images/person_` + getRandomInt(1, 9) + `.jpg" />
                    <p class="donation-amount">` + value.contribution + `</p>
                    </div>`;

      });
      $("#donate-results").html(donator);
    },
    error: function (XMLHttpRequest, textStatus, errorThrown) {
      console.log("Error : " + textStatus + " Threw : " + errorThrown);
    }
  });
}
