for pair in "en_zh" "en_fr" "en_ja" "zh_en" "fr_en" "ja_en"
do
    mkdir "experiment_logs/"$pair
    echo "$pair created"
    
    for dim in 32 64 256 512
    do
        python dbp15k-pipeline.py --category $pair --dim $dim > "experiment_logs/"$pair"/dim.$dim"
        echo "$dim"
    done
    echo "dim done"
    
    for num_layers in 2 3 4 5 6 7
    do
        python dbp15k-pipeline.py --category $pair --num_layers $num_layers > "experiment_logs/"$pair"/num_layers."$num_layers".log"
        echo "$num_layers"
    done
    echo "num_layers done"
    
    for num_steps in 5 10 20 30 40
    do
        python dbp15k-pipeline.py --category $pair --num_steps $num_steps > "experiment_logs/"$pair"/num_steps."$num_steps".log"
        echo "$num_steps"
    done
    echo "num_steps done"
    
    for rnd_dim in 8 16 32 64 128
    do
        python dbp15k-pipeline.py --category $pair --rnd_dim $rnd_dim > "experiment_logs/"$pair"/rnd_dim."$rnd_dim".log"
        echo "$rnd_dim"
    done
    echo "rnd_dim done"
    
    for train_size in 100 300 500 1000 2000 4000 8000
    do
        python dbp15k-pipeline.py --category $pair --train_size $train_size > "experiment_logs/"$pair"/train_size."$train_size".log"
        echo "$train_size"
    done
    echo "train_size done"
    
done