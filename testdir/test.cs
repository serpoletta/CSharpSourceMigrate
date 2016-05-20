class Program
{
    static void Main()
    {
        ElectricGuitar guit1 = new ElectricGuitar();
        Console.WriteLine(guit1.repr());

        Console.WriteLine("Press any key to exit.");
        Console.ReadKey();

    }
}