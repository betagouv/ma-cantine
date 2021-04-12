jest.mock('node-fetch');
const fetch = require('node-fetch');
const { Response, Headers } = jest.requireActual('node-fetch');
const { when } = require('jest-when');

const { createBetaTester } = require('../../application/beta-tester');

describe("Beta-tester creation", () => {

  it("successfully makes GET request to third party API", async () => {
    // prepare function arguments
    const request = {
      payload: {
        keyMeasures: [
          {
            shortTitle: "Test measure 1",
            subMeasures: [{
              shortTitle: "Test sub measure 1",
              status: "done"
            }]
          },
          {
            shortTitle: "Test measure 2",
            subMeasures: [{
              shortTitle: "Test sub measure 2"
            }]
          }
        ],
        form: {
          school: "Test school",
          city: "<b>Dangerous input</b>",
          email: "requester@test.com"
        }
      }
    };
    const hFake = {
      response(json) {
        this.result = json;
        return this;
      },
      code(number) {
        this.statusCode = number;
        return this;
      }
    }

    // mock fetch call
    const responseBodyJSON = { message: "test" };
    const sendinblueRequest = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "api-key": undefined
      },
      body: JSON.stringify({
        sender: { email: undefined, name: "site web ma cantine" },
        to: [{ email: undefined }],
        replyTo: { email: undefined },
        subject: "Nouveau Béta-testeur ma cantine",
        htmlContent: "<!DOCTYPE html> <html> <body><p><b>Cantine:</b> Test school</p>"+
                     "<p><b>Ville:</b> &lt;b&gt;Dangerous input&lt;/b&gt;</p>"+
                     "<p><b>Email:</b> requester@test.com</p><p><b>Téléphone:</b> </p><p><b>Message:</b></p><p></p>"+
                     "<p><b>Test measure 1 :</b></p><p>Test sub measure 1 : done</p>"+
                     "<p><b>Test measure 2 :</b></p><p>Test sub measure 2 : </p>"+
                     "</body> </html>"
      })
    }
    when(fetch).
      calledWith("https://api.sendinblue.com/v3/smtp/email", sendinblueRequest).
      mockReturnValue(
        Promise.resolve(new Response(JSON.stringify(responseBodyJSON), {
            status: 201,
            headers: new Headers({
              'Content-Type': 'application/json'
            })
          }
        ))
      );

    // run tests
    const res = await createBetaTester(request, hFake);

    expect(res.statusCode).toBe(201);
    expect(res.result).toStrictEqual(responseBodyJSON);
    expect(fetch).toHaveBeenCalledTimes(1);
  });

  it("throws error when missing data in payload", async () => {
    await expect(createBetaTester({ payload: {} }, {})).rejects.toThrow();
    await expect(createBetaTester({ payload: { keyMeasures: [] } }, {})).rejects.toThrow();
    const validMeasuresInvalidForm = {
      payload: {
        keyMeasures: [
          { subMeasures: [] }
        ]
      }
    };
    await expect(createBetaTester(validMeasuresInvalidForm, {})).rejects.toThrow();
    await expect(createBetaTester({ payload: { form: {} } }, {})).rejects.toThrow();
  });
});
