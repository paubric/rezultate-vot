using System.IO;
using System.Threading.Tasks;
using ElectionResults.Core.Infrastructure;
using ElectionResults.Core.Services.BlobContainer;
using Microsoft.Azure.WebJobs;
using Microsoft.Extensions.Logging;

namespace ElectionResults.DataProcessing
{
    public class ResultsProcessor
    {
        private readonly IBlobProcessor _blobProcessor;

        public ResultsProcessor(IBlobProcessor blobProcessor)
        {
            _blobProcessor = blobProcessor;
        }

        [FunctionName("ResultsProcessor")]
        public async Task Run([BlobTrigger("%BlobContainerName%/{name}", Connection = "")]
            Stream csvStream, string name, ILogger log, ExecutionContext context)
        {
            FunctionSettings.Initialize(context);
            await _blobProcessor.ProcessStream(csvStream, name);
        }
    }
}
