import Header from '../../components/Header/Header';

const PageTemplate = ({ children }) => {
  return (
    <>
      <Header />
      <div>
        {children}
      </div>
    </>
  );
};

export default PageTemplate;