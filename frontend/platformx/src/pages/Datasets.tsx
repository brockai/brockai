import Tabs from '../components/Tabs';
import Dashboard from '../components/Dashboards';
import Datasets from '../components/Datasets';

const DefaultLayout = () => {

  const tabs = [
    // {
    //   label: 'Dashboard',
    //   content: <Dashboard />,
    // },
    {
      label: 'Datasets',
      content: <Datasets />,
    },
    {
      label: 'Platform API',
      content: <div>Content for Tab 3</div>,
    },
    {
      label: 'Settings',
      content: <div>Content for Tab 3</div>,
    },
  ];

  return (
    <div className="dark:bg-boxdark-2 dark:text-bodydark">
      <div className="flex h-screen overflow-hidden">
        <div className="relative flex flex-1 flex-col overflow-y-auto overflow-x-hidden">
          {/* <div className="container mx-auto p-4">
            <Tabs tabs={tabs} />
          </div> */}
        </div>
      </div>
    </div>
  );
};

export default DefaultLayout;
