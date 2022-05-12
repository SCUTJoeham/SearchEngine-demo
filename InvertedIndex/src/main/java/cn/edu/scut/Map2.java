package cn.edu.scut;

import java.io.IOException;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class Map2 extends Mapper<Text, Text, Text, Text>{
    private Text OutKey = new Text();
    private Text OutValue = new Text();
    public void map(Text key, Text value, Context context)
            throws IOException, InterruptedException {
        int splitIndex = key.toString().indexOf(";");
        OutValue.set(key.toString().substring(splitIndex + 1) + "#" + value);
        OutKey.set(key.toString().substring(0, splitIndex));
        context.write(OutKey, OutValue);
    }
}
