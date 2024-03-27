import loader from "./loader.svg";
import { useState } from "react";
import axios from "axios";

function UI() {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const sendDoc = async (ev) => {
    setLoading(true);
    try {
      const formData = new FormData();
      const file = ev.target.files[0];
      formData.append("doc", file);
      const res = await axios.post("http://localhost:8000/doc", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setStep(2);

      if (res.status !== 200) {
        throw new Error("Network response was not ok");
      }
      setLoading(false);
    } catch (e) {
      console.error("Error:", e);
      setLoading(false);
    }
  };

  const sendQuestions = async (ev) => {
    setLoading(true);
    try {
      const formData = new FormData();
      const file = ev.target.files[0];
      formData.append("questions", file);
      const res = await axios.post("http://localhost:8000/questions", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      if (res?.status !== 200) {
        throw new Error("Network response was not ok");
      }

      setResult(res.data);
      setStep(3);
      setLoading(false);
    } catch (e) {
      console.error("Error:", e);
      setLoading(false);
    }
  };
  return (
    <div className="flex w-screen h-screen justify-center flex-col px-20">
      {!loading && (
        <div className="flex w-full">
          {step === 1 && (
            <div className="flex flex-col w-full">
              <label for="dataDoc" className="text-3xl font-semibold">
                Select document over which the questions will be answered. <br />
                (PDF or JSON only!)
              </label>
              <input
                type="file"
                id="dataDoc"
                accept="application/json,application/pdf"
                onChange={sendDoc}
                className="mx-auto mt-12 text-sm"
              ></input>
            </div>
          )}
          {step === 2 && (
            <div className="flex flex-col w-full">
              <label for="dataDoc" className="text-3xl font-semibold">
                Select questions to be answered. <br />
                (JSON only!)
              </label>
              <input
                type="file"
                id="dataDoc"
                accept="application/json"
                onChange={sendQuestions}
                className="mx-auto mt-12 text-sm"
              ></input>
            </div>
          )}
          {step === 3 && <div className="w-full text-xl">{JSON.stringify(result)}</div>}
        </div>
      )}
      {loading && <img src={loader} alt="loader" className="w-40 m-auto" />}
    </div>
  );
}

export default UI;
