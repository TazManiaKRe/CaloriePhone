import React, { useState, useEffect } from "react";
import './App.css';
import { AppBar, Button, ThemeProvider, Input, Checkbox, FormGroup, FormControlLabel, Box } from "@material-ui/core";
import { createMuiTheme } from "@material-ui/core";
import axios from 'axios';

function PredictionList(props) {

  const [total, setTotal] = useState(JSON.parse(JSON.stringify(props.predictions)));

  useEffect(() => {
    setTotal(props.predictions);
  }, [props.predictions]);

  return (
    <div>
      {typeof (props.predictions) !== 'undefined' &&
        <div>
          {typeof (total) !== 'undefined' &&
            <h3>Total: {Object.keys(total).map(label => { return total[label] }).reduce((a, b) => a + b, 0)} cal</h3>
          }
          <FormGroup>
            {
              Object.keys(props.predictions).map(prediction_label => {
                return (
                  <FormControlLabel
                    control={<Checkbox defaultChecked color="primary" />}
                    label={prediction_label.charAt(0).toUpperCase() + prediction_label.slice(1).replace(/_/g, " ") + " (" + props.predictions[prediction_label] + " cal)"}
                    onChange={e => {
                      let newtotal = {...total}
                      if (e.target.checked) {
                        newtotal[prediction_label] = props.predictions[prediction_label]
                      } else {
                        newtotal[prediction_label] = 0
                      }
                      setTotal(newtotal)
                    }}
                  />
                )
              })
            }
          </FormGroup>
        </div>}
    </div >
  )

}

function App() {

  const [file, setFile] = useState();
  const [data, setData] = useState();
  const [total, setTotal] = useState();

  async function getPrediction(image_file) {

    // send image to backend for prediction
    const res = await axios({
      method: "post",
      url: "/prediction",
      data: image_file,
      headers: { "Content-Type": image_file.type },
    })

    setData(res.data);
  }

  function handleChange(e) {
    setFile(URL.createObjectURL(e.target.files[0]));
    getPrediction(e.target.files[0])
  }

  useEffect(() => {
    document.title = "Caloriephone"
  }, [])

  return (
    <div className="App">
      <ThemeProvider theme={createMuiTheme({ palette: { primary: { main: "#cbe4f9" }, secondary: { main: "#cdf5f6" } } })}>

        <AppBar color="primary"><h2>Caloriephone</h2></AppBar>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          marginTop: '7%'
        }}>
          <label htmlFor="contained-button-file">
            <Input accept="image/*" id="contained-button-file" type="file" onChange={handleChange} style={{ display: 'none' }} />
            <Button variant="contained" component="span" color="primary">
              Upload
            </Button>
          </label>
        </div>
        <Box 
          component="img"
          sx={{
            maxHeight: "50%",
            maxWidth: "50%",
            marginTop: "2%"
          }}
          src={file}
        />
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}>
          {typeof data !== 'undefined' &&
            <div style={{ width: "400px" }}>
              <PredictionList predictions={data} ></PredictionList>
            </div>
          }
        </div>
      </ThemeProvider>
    </div>

  );
}

export default App;