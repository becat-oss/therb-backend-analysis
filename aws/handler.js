var AWS = require('aws-sdk')
var s3 = new AWS.S3()

exports.handler = async (event) => {

    var params = {
        Bucket: "バケット名", 
        Key: "ZIPファイル名"
    };

    const zip_data = await s3.getObject(params).promise()

    const response = {
        statusCode: 200,
        "headers": {
            "Content-Disposition": 'attachment; filename="download_filename.zip"',
            "Content-Type": 'application/zip'
        },
        // base64でテキストに変換している。
        body: zip_data.Body.toString('base64'),
        isBase64Encoded: true
    }

    return response;
}