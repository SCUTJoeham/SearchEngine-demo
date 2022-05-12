package cn.edu.scut;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;

import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.KeyValueTextInputFormat;
import org.apache.hadoop.mapreduce.lib.jobcontrol.ControlledJob;
import org.apache.hadoop.mapreduce.lib.jobcontrol.JobControl;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.IOException;

public class MRMain
{
    public static void main( String[] args )
            throws IOException, InterruptedException, ClassNotFoundException {
        if(args.length != 3) {
            System.out.println("Please Enter Parameters: [InputPath] [OutputPath1] [OutputPath2]");
            System.exit(1);
        }

        Configuration conf1 = new Configuration();
        Configuration conf2 = new Configuration();

        Path inputPath = new Path(args[0]);
        Path interOutputPath = new Path(args[1]);
        Path finalOutputPath = new Path(args[2]);

        FileSystem fs=FileSystem.get(conf1);

        if (fs.exists(interOutputPath)) {
            fs.delete(interOutputPath, true);
        }

        if (fs.exists(finalOutputPath)) {
            fs.delete(finalOutputPath, true);
        }

        Job job1 = Job.getInstance(conf1);
        Job job2 = Job.getInstance(conf2);

        job1.setJarByClass(MRMain.class);
        job1.setMapperClass(Map1.class);
        job1.setReducerClass(Reduce1.class);
        job1.setOutputKeyClass(Text.class);
        job1.setOutputValueClass(IntWritable.class);

        job1.setInputFormatClass(KeyValueTextInputFormat.class);
        FileInputFormat.setInputPaths(job1, inputPath);
        FileOutputFormat.setOutputPath(job1, interOutputPath);

        job2.setJarByClass(MRMain.class);
        job2.setMapperClass(Map2.class);
        job2.setReducerClass(Reduce2.class);
        job2.setOutputKeyClass(Text.class);
        job2.setOutputValueClass(Text.class);

        job2.setInputFormatClass(KeyValueTextInputFormat.class);
        FileInputFormat.setInputPaths(job2, interOutputPath);
        FileOutputFormat.setOutputPath(job2, finalOutputPath);

        JobControl jobControl = new JobControl("jc");

        ControlledJob controlledJob1 = new ControlledJob(job1.getConfiguration());
        ControlledJob controlledJob2 = new ControlledJob(job2.getConfiguration());
        controlledJob1.setJob(job1);
        controlledJob2.setJob(job2);

        controlledJob2.addDependingJob(controlledJob1);

        jobControl.addJob(controlledJob1);
        jobControl.addJob(controlledJob2);

        Thread jobControlThread = new Thread(jobControl);
        jobControlThread.setDaemon(true);

        long start = System.currentTimeMillis();
        jobControlThread.start();

        while(true) {
            if (jobControl.allFinished()) {
                long end = System.currentTimeMillis();
                double during = (end-start)/1000.0;
                System.out.println(jobControl.getSuccessfulJobList());
                System.out.println("Total Cost: " + during + "s");
                System.exit(0);
            }
        }
    }
}
