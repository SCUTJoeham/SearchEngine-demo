package cn.edu.scut;

import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class Map1 extends Mapper<Text, Text, Text, IntWritable>{

    private Text OutKey = new Text();
    private IntWritable OutValue = new IntWritable();
    @Override
    public void map(Text key, Text value, Context context)
        throws IOException, InterruptedException {
        String[] tokens = value.toString().split(" ");
        for(String tk : tokens) {
            OutKey.set(tk + ";" + key);
            OutValue.set(1);
            context.write(OutKey, OutValue);
        }
    }

}
