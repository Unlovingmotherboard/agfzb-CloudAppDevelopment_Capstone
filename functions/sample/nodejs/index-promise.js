/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

function main(params) {

    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);

    let dbListPromise = getAllRecords(cloudant, "dealerships");
    return dbListPromise;
}

function getDbs(cloudant) {
     return new Promise((resolve, reject) => {
         cloudant.getAllDbs()
             .then(body => {
                 resolve({ dbs: body.result });
             })
             .catch(err => {
                  console.log(err);
                 reject({ err: err });
             });
     });
 }
 
                        
 /*
 Sample implementation to get all the records in a db.
 */
 function getAllRecords(cloudant,dbname) {
    return new Promise((resolve, reject) => {
        cloudant.postAllDocs({ db: dbname, includeDocs: true, limit: 10 })        
            .then((result)=>{
              resolve({result:result.result.rows});
            })
            .catch(err => {
               if(err.statusCode === 404) {
                   reject({error:'Dataqbase not found'});
               } else if (err.statusCode === 500) {
                   reject({error:'Internal server error'});
               }
                 else {
                   reject({ err: err });
                 }
            });
        });
}
function getAllRecordsByState(cloudant, dbname, state) {

    const selector = {
        'state': state
    }
    console.log(selector)
    return new Promise((resolve, reject) => {
        cloudant.postFind({
            db: dbname,
            selector: selector
        }).then((result)=>{
              resolve({result:result.result.docs});
            })
            .catch(err => {
               if(err.statusCode === 404) {
                   reject({error:'Database not found'});
               } else if (err.statusCode === 500) {
                   reject({error:'Internal server error'});
               }
                 else {
                   reject({ err: err });
                 }
            })
    })
}