const table1Button = document.querySelector('#customers');
const tableContainer = document.querySelector('#table-container');


table1Button.addEventListener('click', () => {
  fetch('/api/customers')
    .then(response => response.json())
    .then(data => {
      let arr = data["customers"]
      tableContainer.innerHTML = `
        <table>
          <thead>
            <tr>
              <th>First name</th>
              <th>Last name</th>
              <th>E-mail</th>
              <th>Phone</th>
            </tr>
          </thead>
          <tbody>
            ${arr.map(row => `
              <tr>
                <td>${row.customer_id}</td>
                <td><input type=text name=first_name value=${row.first_name}></td>
                <td><input type=text name=last_name value=${row.last_name}></td>
                <td><input type=text name=email value=${row.email}></td>
                <td><input type=text name=phone value=${row.phone}></td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;
    });
});