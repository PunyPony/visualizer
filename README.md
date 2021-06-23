Data:

Please put the NIfTI files in the provided /data/images /data/masks folders.
Images and their associated mask must have the same name.

Run the App:

You can launch this by executing the provided launch.sh script.
This Django app run into a docker container.

Features:

This application provide 3 features:

GET /slice_[XYZ]/<slice_Nb>/<file_name>
- Visualize a slice of a NIfTI file

GET /histogram/<file_name>
- Draw the histogram of a NIfTI file (values are rescaled between 0 and 255)

GET /histogram/<file_name>/<mask_name>
- Apply a mask to its related scan then draw its histogram (values are rescaled between 0 and 255)

These 3 features are also available with a web interface using the route /home