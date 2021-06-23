Data:

Put the NIfTI files in the provided /data/images /data/masks folders.
Images and their associated masks must have the same name.

Run the App:

You can launch this web App by executing the provided launch.sh script.
This will instanciate a docker container and run the app in it.

Features:

This application provide 3 features:

GET /slice_[XYZ]/<slice_Nb>/<file_name>
- Visualize a slice of a NIfTI file

GET /histogram/<file_name>
- Draw the histogram of a NIfTI file (values are rescaled between 0 and 255)

GET /histogram/<file_name>/<mask_name>
- Apply a mask to its related scan and then draw its histogram (values are rescaled between 0 and 255)

These 3 features are also available with a web interface using the route /home
