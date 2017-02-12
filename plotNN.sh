declare -a starID
let i=0
while IFS=$'\n' read -r line_data; do
    # Parse “${line_data}” to produce content 
    starID[i]="${line_data}" # Populate array.
    ((++i))
done < nearestStars.txt
echo i


let x=0
while IFS=$'\n' read -r object; do
python PlotNNstar.py -id ${object} -starid ${starID[x]}


echo "ran routine"
((++x))
echo x ${object} ${startID[x]}
done < qsos.txt