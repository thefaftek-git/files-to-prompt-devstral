using System;
using System.IO;

class FileUtils
{
    public static string ReadFile(string path)
    {
        return File.ReadAllText(path);
    }

    public static void WriteFile(string path, string data)
    {
        File.WriteAllText(path, data);
    }

    public static void AppendFile(string path, string data)
    {
        File.AppendAllText(path, data);
    }

    public static void DeleteFile(string path)
    {
        File.Delete(path);
    }

    public static bool DoesFileExist(string path)
    {
        return File.Exists(path);
    }

    public static string[] GetFilesInDirectory(string dir)
    {
        return Directory.GetFiles(dir);
    }

    static void Main()
    {
        Console.WriteLine("Sample CS file");
        Console.WriteLine("Another line");
        Console.WriteLine("Yet another line");
        Console.WriteLine("This is line 5");
        Console.WriteLine("This is line 6");
        Console.WriteLine("More content");
        Console.WriteLine("Additional lines");
        Console.WriteLine("Keep adding lines");
        Console.WriteLine("Line 10");
        Console.WriteLine("Line 11");
        Console.WriteLine("Line 12");
    }
}