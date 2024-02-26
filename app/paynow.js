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
var BACKEND_URL = new URL(window.location.origin)
BACKEND_URL.search = ''
BACKEND_URL.pathname = '/api/v1/transactions'
var BACKEND = BACKEND_URL.toString()
console.log("BACKEND: " + BACKEND);

// Used to select random people photos
function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1) + min);
}

// Get current donations on page load
$(document).ready(getDonations());

// When the website user clicks the donate button, send their details
// to the backend and update the page
$("#paynowButton").click(function () {

  var donateJSON = {
    name: $('#formName').val(),
    email: $('#formEmail').val(),
    location: $('#formCountry').val(),
    contribution: $('#paymentAmount').val(),
    creditCardNumber: $('#ccNum').val(),
    creditCardCVV: $('#ccCVV').val()
  };

  console.log("Sending : " + JSON.stringify(donateJSON));

  $.ajax({
    type: "POST",
    url: BACKEND + "",
    contentType: "application/json; charset=utf-8",
    data: JSON.stringify(donateJSON),
    success: function (msg) {

      // Change the button text
      $("#paynowButton").prop('value', 'Thank you!');

      // Clear the fields
      $('#formName').prop('value', '');
      $('#formEmail').prop('value', '');
      $('#ccNum').prop('value', '');
      $('#ccCVV').prop('value', '');
      $('#paymentAmount').prop('value', '$');

      // Scroll down to show the donation results
      setTimeout(function () {
        // Get the current donations again (repopulate the HTML)
        getDonations();

        // Change the donation button back
        $("#paynowButton").prop('value', 'PayNow');
      }, 1000);
    },
    error: function (XMLHttpRequest, textStatus, errorThrown) {
      console.log("Error : " + textStatus + "Error Thrown : " + errorThrown);
    }
  });
});



// Fetch the PayNow from the backend database and insert it into
// the donations page.
function getDonations() {
  $.ajax({
    type: "GET",
    url: BACKEND + "",
    dataType: "json",
    success: function (msg) {
      console.log("Success : " + JSON.stringify(msg));

      // No new payments, try again in a few seconds
      if (msg.length == 0) {
        console.log("Backend DB empty");
        $("#paynow-results").html(`<p class="zero">You have not made any payments yet. Try it now!</p>`);
        return;
      }

      var donatorList = msg.reverse();
      console.log("Success. Retrieved " + msg.length + " records from backend");

      // Chopping it up so we only show latest 5 contributions
      // console.log(donatorList.slice(0, (donatorList.length < 5 ? donatorList.length : 5)));
      var donator = "";
      var status ="Settled"
      $.each(donatorList, function (index, value) {

        donator = donator + `<div class="paynow">
                    <p class="name">` + value.name + `</p>
                    <img src="images/person_` + getRandomInt(1, 9) + `.jpg" />
                    <p class="payment-amount">` + value.contribution + `</p>
                    <p class="payment-amount">Payment status: ` + status + `</p>
                    </div>`;

      });
      $("#paynow-results").html(donator);
    },
    error: function (XMLHttpRequest, textStatus, errorThrown) {
      console.log("Error : " + textStatus + " Threw : " + errorThrown);
    }
  });
}
