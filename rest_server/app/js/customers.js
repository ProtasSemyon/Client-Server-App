const table1Button = document.querySelector('#customers');
const tableContainer = document.querySelector('#table-container');


table1Button.addEventListener('click', () => {
  fetch('/api/customers')
    .then(response => response.json())
    .then(data => {
      tableContainer.innerHTML = `
        <table>
          <thead>
            <tr>
              <th></th>
              <th>First name</th>
              <th>Last name</th>
              <th>E-mail</th>
              <th>Phone</th>
            </tr>
          </thead>
          <tbody>
          </tbody>
        </table>
          `
      const myTableBody = tableContainer.querySelector('tbody');

      let arr = data["customers"];
      arr.forEach(item => {
        const row = document.createElement('tr');
        const idCell = document.createElement('td');
        idCell.textContent = item.customer_id;
        const firstNameCell = document.createElement('td');
        const lastNameCell = document.createElement('td');
        const emailCell = document.createElement('td');
        const cityCell = document.createElement('td');

        const updateButtonCell = document.createElement('td');
        const updateButton = document.createElement('button');
        updateButton.textContent = 'Update';

        const deleteButtonCell = document.createElement('td');
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';

        const firstNameInput = document.createElement('input')
        firstNameInput.setAttribute('type', 'text')
        firstNameInput.setAttribute('value', item.first_name);
        const lastNameInput = document.createElement('input')
        lastNameInput.setAttribute('type', 'text')
        lastNameInput.setAttribute('value', item.last_name);
        const emailInput = document.createElement('input')
        emailInput.setAttribute('type', 'text')
        emailInput.setAttribute('value', item.email);
        const phoneInput = document.createElement('input')
        phoneInput.setAttribute('type', 'text')
        phoneInput.setAttribute('value', item.phone);

        firstNameCell.appendChild(firstNameInput);
        lastNameCell.appendChild(lastNameInput);
        emailCell.appendChild(emailInput);
        cityCell.appendChild(phoneInput);

        updateButtonCell.appendChild(updateButton);
        deleteButtonCell.appendChild(deleteButton);

        row.appendChild(idCell);
        row.appendChild(firstNameCell);
        row.appendChild(lastNameCell);
        row.appendChild(emailCell);
        row.appendChild(cityCell);
        row.appendChild(updateButtonCell);
        row.appendChild(deleteButton);
        myTableBody.appendChild(row);
      });
      const row = document.createElement('tr');
      const idCell = document.createElement('td');
      const firstNameCell = document.createElement('td');
      const lastNameCell = document.createElement('td');
      const emailCell = document.createElement('td');
      const cityCell = document.createElement('td');

      const addButtonCell = document.createElement('td');
      const addButton = document.createElement('button');
      addButton.textContent = 'Add';

      const firstNameInput = document.createElement('input')
      firstNameInput.setAttribute('type', 'text')
      firstNameInput.setAttribute('value', '');

      const lastNameInput = document.createElement('input')
      lastNameInput.setAttribute('type', 'text')
      lastNameInput.setAttribute('value', '');

      const emailInput = document.createElement('input')
      emailInput.setAttribute('type', 'text')
      emailInput.setAttribute('value', '');

      const phoneInput = document.createElement('input')
      phoneInput.setAttribute('type', 'text')
      phoneInput.setAttribute('value', '');


      firstNameCell.appendChild(firstNameInput);
      lastNameCell.appendChild(lastNameInput);
      emailCell.appendChild(emailInput);
      cityCell.appendChild(phoneInput);

      addButton.addEventListener('click', () => {
        const dataForAdd = {
          first_name: firstNameInput.textContent, 
          last_name: lastNameInput.textContent, 
          email: emailInput.textContent,
          phone: phoneInput.textContent
        };
        // отправляем данные на сервер через AJAX-запрос
        fetch('/api/customers', {
          method: 'PUT',
          body: JSON.stringify(dataForAdd),
          headers: {
            'Content-Type': 'application/json'
          }
        })
        .then(response => {
          if (response.ok) {
            console.log('Данные успешно обновлены');
          } else {
            console.error('Произошла ошибка при обновлении данных');
          }
        })
        .catch(error => {
          console.error('Произошла ошибка при отправке запроса на сервер', error);
        });
      });

      addButtonCell.appendChild(addButton);

      row.appendChild(idCell);
      row.appendChild(firstNameCell);
      row.appendChild(lastNameCell);
      row.appendChild(emailCell);
      row.appendChild(cityCell);
      row.appendChild(addButtonCell);
      myTableBody.appendChild(row);
    });
});