package cn.edu.scut;

import java.io.IOException;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class Reduce2 extends Reducer<Text, Text, Text, Text>{

    private Text OutValue = new Text();
    @Override
    protected void reduce(Text key, Iterable<Text> values, Context context)
            throws IOException, InterruptedException {
        String urlList = new String();

        for(Text url : values){
            urlList += url.toString() + ";";
        }
        OutValue.set(urlList);
        context.write(key, OutValue);
    }
}
