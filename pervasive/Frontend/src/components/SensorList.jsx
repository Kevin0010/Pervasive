import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

const SensorLists = () => {
  const [sensors, setSensors] = useState([]);

  useEffect(() => {
    getSensors();
  }, []);

  const getSensors = async () => {
    const response = await axios.get("http://localhost:5000/sensors");
    setSensors(response.data);
  };

  const deleteSensor = async (sensorId) => {
    await axios.delete(`http://localhost:5000/sensors/${sensorId}`);
    getSensors();
  };

  return (
    <div>
      <h1 className="title">Sensors</h1>
      <h2 className="subtitle">List of Sensors</h2>
      <Link to="/sensors/add" className="button is-primary mb-2">
        Add New
      </Link>
      <table className="table is-striped is-fullwidth">
        <thead>
          <tr>
            <th>No</th>
            <th>Sensor Name</th>
            <th>Created By</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {sensors.map((sensor, index) => (
            <tr key={sensor.uuid}>
              <td>{index + 1}</td>
              <td>{sensor.name}</td>
              <td>{sensor.user.name}</td>
              <td>
                <Link
                  to={`/sensors/edit/${sensor.uuid}`}
                  className="button is-small is-info"
                >
                  Edit
                </Link>
                <button
                  onClick={() => deleteSensor(sensor.uuid)}
                  className="button is-small is-danger"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default SensorLists;
