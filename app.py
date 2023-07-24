from flask import Flask, request, send_file
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/remove-background', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return 'No image provided', 400

    file = request.files['image']

    # convert file to Image
    input = Image.open(file.stream)

    # remove background
    output = remove(input)

    # calculate new height based on original aspect ratio
    width_percent = (200/float(output.size[0]))
    new_height = int((float(output.size[1])*float(width_percent)))

    # resize the image while keeping aspect ratio
    # output = output.resize((200, new_height))

    # save the result image to a byte stream
    output_io = io.BytesIO()
    output.save(output_io, format='WEBP')
    output_io.seek(0)

    return send_file(output_io, mimetype='image/webp')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
