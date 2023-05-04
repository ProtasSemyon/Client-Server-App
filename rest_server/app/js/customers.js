const customersButton = document.querySelector('#customers');
tableContainer = document.querySelector('#table-container');
const customersUrl = '/api/customers'

function clearHtml() {
  tableContainer.innerHTML = '';
}

function addRow_customers(item, tableBody) {
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

  updateButton.addEventListener('click', () => {
    const dataForAdd = {
      customer_id: idCell.textContent, 
      first_name: firstNameInput.value, 
      last_name: lastNameInput.value, 
      email: emailInput.value,
      phone: phoneInput.value
    };

    fetch(customersUrl + '/' + idCell.textContent, {
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
      return response.json()
    }).then(data => {
      console.log(data);
      fillTableContainer_customers(data);
    })
    .catch(error => {
      console.error('Произошла ошибка при отправке запроса на сервер', error);
    });
  })

  deleteButton.addEventListener('click', () => {
    fetch(customersUrl + '/' + idCell.textContent, {
      method: 'DELETE',
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
      return response.json()
    }).then(data => {
      console.log(data);
      fillTableContainer_customers(data);
    })
    .catch(error => {
      console.error('Произошла ошибка при отправке запроса на сервер', error);
    });
  })

  updateButtonCell.appendChild(updateButton);
  deleteButtonCell.appendChild(deleteButton);

  row.appendChild(idCell);
  row.appendChild(firstNameCell);
  row.appendChild(lastNameCell);
  row.appendChild(emailCell);
  row.appendChild(cityCell);
  row.appendChild(updateButtonCell);
  row.appendChild(deleteButton);
  tableBody.appendChild(row);
}

function addButton_customers(tableBody) {
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
      first_name: firstNameInput.value, 
      last_name: lastNameInput.value, 
      email: emailInput.value,
      phone: phoneInput.value
    };

    fetch(customersUrl, {
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
      return response.json()
    }).then(data => {
      console.log(data);
      fillTableContainer_customers(data);
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
  tableBody.appendChild(row);
}

function fillTableContainer_customers(data) {
  clearHtml()
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
  let arr = data["customers"];
  const tableBody = tableContainer.querySelector('tbody');

  arr.forEach(item => addRow_customers(item, tableBody));
  addButton_customers(tableBody)
}

customersButton.addEventListener('click', () => {
  fetch(customersUrl)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      fillTableContainer_customers(data);
})});