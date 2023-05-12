import cv2
import numpy as np
from tqdm import tqdm

def ascii_video(video_file, output_file):
    cap = cv2.VideoCapture(video_file)

    # Get the width and height of the video frames
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, 30.0, (width, height), isColor=False)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    for i in tqdm(range(total_frames)):
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Resize the frame to the desired width and height
        gray_resized = cv2.resize(gray, (width, height))

        # Convert the resized frame to ascii art
        ascii_frame = ascii_art(gray_resized, width, height)

        # Convert the ascii_frame string to a NumPy array
        ascii_array = np.array([list(map(ord, line)) for line in ascii_frame.splitlines()], dtype=np.uint8)

        # Write the frame to the output video file
        out.write(ascii_array)

    # Release the video capture and writer objects
    cap.release()
    out.release()

    print("Done!")


def ascii_art(image, width=100, height=100):
    # Check number of channels
    if image.ndim == 3 and image.shape[2] == 3:
        # Convert BGR to grayscale
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        palette = [' ', '.', '*', ':', 'o', '&', '8', '#', '@']
    elif image.ndim == 2:
        # Input image is already grayscale
        grayscale_image = image
        palette = [' ', '.', '*', ':', 'o', '&', '8', '#', '@']
    else:
        raise ValueError('Input image must have either one or three channels')

    # Resize image
    resized_image = cv2.resize(grayscale_image, (width, height))

    # Convert to ASCII art
    ascii_chars = [[palette[int(pixel / 25)] for pixel in row] for row in resized_image]
    ascii_art = '\n'.join([''.join(row) for row in ascii_chars])

    return ascii_art


if __name__ == '__main__':
    # Set the file paths.
    video_file = 'video.mp4'
    output_file = 'output_video.avi'

    # Convert the video to ASCII video.
    ascii_video(video_file, output_file)

    # Print a message to the user.
    print('The video has been converted to ASCII video.')
